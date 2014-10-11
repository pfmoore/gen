import subprocess

def test_basic(tmpdir):
    template = tmpdir / 'template.yaml'
    template.write_text("name: foo\ncontent: bar", encoding='ascii')
    subprocess.check_call(['gen.exe', '--target', str(tmpdir), str(template)])
    assert (tmpdir / 'foo').read() == 'bar'
