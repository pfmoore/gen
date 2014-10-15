import os
import io
import stat
import yaml

def ensuredir(name):
    """Make sure directory name exists.

    Code lifted (and hugely simplified) from os.makedirs.
    
    """
    head, tail = os.path.split(name)
    if not tail:
        head, tail = os.path.split(head)
    if head and tail and not os.path.exists(head):
        ensuredir(head)
    if not os.path.isdir(name):
        os.mkdir(name)

def build(filename, content=None, directory=False, encoding='utf-8', executable=False, target=None):
    if target:
        filename = os.path.join(target, filename)
    dirname, basename = os.path.split(filename)
    ensuredir(dirname)
    if not basename:
        return
    if directory:
        os.mkdir(filename)
        return
    with io.open(filename, 'w', encoding=encoding) as f:
        if content:
            f.write(content)
    if executable:
        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR)

# Build a file. Information needed:
#   - filename
#   - type (directory or file)
#   - content (Maybe later - function to generate streamed content?)
#   - encoding
#   - executable
#
def build_one_file(defn, cwd=None):
    if 'name' not in defn:
        raise ValueError("Invalid definition - no filename")
    filename = defn.pop('name')

    build(filename, target=cwd, **defn)

def build_files(defn, cwd=None):
    for defn in yaml.safe_load_all(defn):
        build_one_file(defn, cwd)
