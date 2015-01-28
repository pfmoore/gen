from gen.generate import build
from gen.loader import FilesystemLoader
import os

def test_filesystem_loader(tmpdir):
    build(dict(name='test/foo', content='Hello, world'), target=str(tmpdir))
    build(dict(name='test/bar', content='Hello, bar'), target=str(tmpdir))
    loader = FilesystemLoader(str(tmpdir))
    templates = sorted(t.replace(os.sep, '/') for t in loader.list_templates())
    assert templates == ['test/bar', 'test/foo']
    assert loader.get_source('test/foo') == 'Hello, world'
