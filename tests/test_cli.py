import subprocess
from gen.generate import build

def test_basic(tmpdir):
    template = tmpdir / 'template.yaml'
    template.write_text("name: foo\ncontent: bar", encoding='ascii')
    subprocess.check_call(['gen.exe', '--target', str(tmpdir), str(template)])
    assert (tmpdir / 'foo').read() == 'bar'

def test_simple_template(tmpdir):
    build('test/foo', content='Hello, world', target=str(tmpdir))
    build('test/bar', content='Hello, bar', target=str(tmpdir))
    dest = tmpdir.mkdir('target')
    subprocess.check_call(
        ['gen.exe', '--target', str(dest), 'test'],
        cwd=str(tmpdir)
    )
    assert len(dest.listdir()) == 2
    assert (dest / 'foo').read_text(encoding='utf-8') == 'Hello, world'
    assert (dest / 'bar').read_text(encoding='utf-8') == 'Hello, bar'
