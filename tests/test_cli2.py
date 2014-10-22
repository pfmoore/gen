from click.testing import CliRunner
from gen import main, __version__
from textwrap import dedent
import subprocess
import py
import sys

def test_run_main():
    result = subprocess.call([sys.executable, '-m', 'gen', '--version'])
    assert result == 0

def test_help():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0

def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert result.output.endswith(__version__ + '\n')

def test_emptyfile():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        tmpl.write(dedent('''
          files:
            - name: foo
        '''))
        result = runner.invoke(main, [str(tmpl)])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(file=1)
        assert out.size() == 0

def test_target():
    runner = CliRunner()
    with runner.isolated_filesystem():
        target = py.path.local('target')
        target.mkdir()
        tmpl = py.path.local('template.yaml')
        tmpl.write(dedent('''
          files:
            - name: foo
        '''))
        # Note: because of the argument parsing for variables, options like
        # --target must go *before* the template name.
        # TODO: See if we can relax this restriction.
        result = runner.invoke(main, ['--target', str(target), str(tmpl)])
        assert result.exit_code == 0
        out = target / 'foo'
        assert out.check(file=1)
        assert out.size() == 0

def test_directory():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        tmpl.write(dedent('''
          files:
            - name: foo
              directory: yes
        '''))
        result = runner.invoke(main, [str(tmpl)])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(dir=1)

def test_directory_shortform():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        tmpl.write(dedent('''
          files:
            - name: foo/
        '''))
        result = runner.invoke(main, [str(tmpl)])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(dir=1)

def test_ascii_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        tmpl.write(dedent('''
          files:
            - name: foo
              content: bar
        '''))
        result = runner.invoke(main, [str(tmpl)])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(file=1)
        assert out.read() == 'bar'

def test_emptyfile_with_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        tmpl.write(dedent('''
          version: 1
          files:
            - name: foo
        '''))
        result = runner.invoke(main, [str(tmpl)])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(file=1)
        assert out.size() == 0

def test_emptyfile_with_wrong_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        tmpl.write(dedent('''
          version: 2
          files:
            - name: foo
        '''))
        result = runner.invoke(main, [str(tmpl)])
        assert result.exit_code != 0

def test_latin1_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        # Note that files in YAML format should be UTF-8 or UTF-16 with a BOM
        tmpl.write_text(dedent('''
          files:
            - name: foo
              content: \xa3
              encoding: latin-1
        '''), encoding='utf-8')
        result = runner.invoke(main, [str(tmpl)])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(file=1)
        assert out.read_binary() == b'\xa3'

def test_utf8_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        # Note that files in YAML format should be UTF-8 or UTF-16 with a BOM
        tmpl.write_text(dedent('''
          files:
            - name: foo
              content: \xa3
              encoding: utf-8
        '''), encoding='utf-8')
        result = runner.invoke(main, [str(tmpl)])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(file=1)
        assert out.read_binary() == b'\xc2\xa3'

def test_utf8_default():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        # Note that files in YAML format should be UTF-8 or UTF-16 with a BOM
        tmpl.write_text(dedent('''
          files:
            - name: foo
              content: \xa3
        '''), encoding='utf-8')
        result = runner.invoke(main, [str(tmpl)])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(file=1)
        assert out.read_binary() == b'\xc2\xa3'

def test_override_default_encoding():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        # Note that files in YAML format should be UTF-8 or UTF-16 with a BOM
        tmpl.write_text(dedent('''
          files:
            - name: foo
              content: \xa3
          defaults:
            encoding: latin-1
        '''), encoding='utf-8')
        result = runner.invoke(main, [str(tmpl)])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(file=1)
        assert out.read_binary() == b'\xa3'

def test_variable_basic():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        tmpl.write(dedent('''
          variables:
            - name: var
          files:
            - name: foo
        '''))
        result = runner.invoke(main, [str(tmpl), '--var', 'abc'])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(file=1)
        assert out.size() == 0

def test_rendering_basic():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        tmpl.write(dedent('''
          variables:
            - name: var
          files:
            - name: foo
              content: value={var}
              renderer: format
        '''))
        result = runner.invoke(main, [str(tmpl), '--var', 'abc'])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(file=1)
        assert out.read_text(encoding='ascii') == 'value=abc'

def test_variable_default():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        tmpl.write(dedent('''
          variables:
            - name: var
              default: abc
          files:
            - name: foo
              content: value={var}
              renderer: format
        '''))
        result = runner.invoke(main, [str(tmpl)])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(file=1)
        assert out.read_text(encoding='ascii') == 'value=abc'

def test_variable_override():
    runner = CliRunner()
    with runner.isolated_filesystem():
        tmpl = py.path.local('template.yaml')
        tmpl.write(dedent('''
          variables:
            - name: var
              default: abc
          files:
            - name: foo
              content: value={var}
              renderer: format
        '''))
        result = runner.invoke(main, [str(tmpl), '--var', 'def'])
        assert result.exit_code == 0
        out = py.path.local('foo')
        assert out.check(file=1)
        assert out.read_text(encoding='ascii') == 'value=def'

# To be considered
# 1. What to do when a variable has no default and is not specified
