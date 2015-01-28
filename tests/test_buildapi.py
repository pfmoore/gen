from gen.generate import build

def test_empty_file(tmpdir):
    """Create an empty file"""
    defn = {'name': 'foo'}
    build(defn, target=str(tmpdir), variables={})
    assert (tmpdir / 'foo').check(file=1)
    assert (tmpdir / 'foo').size() == 0

def test_empty_dir(tmpdir):
    """Create an empty directory"""
    defn = {'name': 'foo', 'directory': True}
    build(defn, target=str(tmpdir), variables={})
    assert (tmpdir / 'foo').check(dir=1)
    assert len((tmpdir / 'foo').listdir()) == 0

def test_empty_dir_trailing_slash(tmpdir):
    """A name with a trailing slash creates an empty directory"""
    defn = {'name': 'foo/'}
    build(defn, target=str(tmpdir), variables={})
    assert (tmpdir / 'foo').check(dir=1)
    assert len((tmpdir / 'foo').listdir()) == 0

def test_text_file(tmpdir):
    """Create a text file"""
    defn = {'name': 'foo', 'content': 'Hello'}
    build(defn, target=str(tmpdir), variables={})
    assert (tmpdir / 'foo').check(file=1)
    assert (tmpdir / 'foo').read_binary() == b'Hello'

def test_utf8_file(tmpdir):
    """Create a text file, ensure default encoding is utf8"""
    funky_char = '\N{Euro sign}'
    defn = {'name': 'foo', 'content': funky_char}
    build(defn, target=str(tmpdir), variables={})
    assert (tmpdir / 'foo').check(file=1)
    assert (tmpdir / 'foo').read_binary() == funky_char.encode('utf-8')

def test_latin1_file(tmpdir):
    """Create a text file, ensure explicit encoding is respected"""
    funky_char = '\N{Pound sign}'
    defn = {'name': 'foo', 'content': funky_char, 'encoding': 'latin-1'}
    build(defn, target=str(tmpdir), variables={})
    assert (tmpdir / 'foo').check(file=1)
    assert (tmpdir / 'foo').read_binary() == funky_char.encode('latin-1')

def test_unicode_filename(tmpdir):
    """Create a file with a Unicode filename"""
    funky_char = '\N{Euro sign}'
    defn = {'name': funky_char}
    build(defn, target=str(tmpdir), variables={})
    assert (tmpdir / funky_char).check(file=1)
    assert (tmpdir / funky_char).size() == 0

