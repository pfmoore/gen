from gen.generate import build
from gen.loader import FilesystemLoader

def test_filesystem_loader(tmpdir):
    build('test/foo', content='Hello, world', target=str(tmpdir))
    build('test/bar', content='Hello, bar', target=str(tmpdir))
    loader = FilesystemLoader(str(tmpdir))
    assert sorted(loader.list_templates()) == ['test\\bar', 'test\\foo']
    assert loader.get_source('test/foo') == 'Hello, world'
