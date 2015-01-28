import subprocess
from gen.generate import build

def test_basic(tmpdir):
    template = tmpdir / 'template.yaml'
    template.write_text("files:\n - name: foo\n   content: bar", encoding='ascii')
    subprocess.check_call(['gen', '--target', str(tmpdir), str(template)])
    assert (tmpdir / 'foo').read_text(encoding='ascii') == 'bar'

def test_simple_template(tmpdir):
    build(dict(name='test/foo', content='Hello, world'), target=str(tmpdir))
    build(dict(name='test/bar', content='Hello, bar'), target=str(tmpdir))
    dest = tmpdir.mkdir('target')
    subprocess.check_call(
        ['gen', '--target', str(dest), 'test'],
        cwd=str(tmpdir)
    )
    assert len(dest.listdir()) == 2
    assert (dest / 'foo').read_text(encoding='ascii') == 'Hello, world'
    assert (dest / 'bar').read_text(encoding='ascii') == 'Hello, bar'
