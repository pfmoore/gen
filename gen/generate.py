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

def build_one_file(defn, cwd=None):
    filename = defn['name']
    if cwd:
        filename = os.path.join(cwd, filename)
    dirname, basename = os.path.split(filename)
    ensuredir(dirname)
    if not basename:
        return
    if defn.get('directory'):
        os.mkdir(filename)
        return
    with io.open(filename, 'w', encoding=defn.get('encoding', 'utf-8')) as f:
        f.write(defn.get('content', ''))
    if defn.get('executable'):
        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR)

def build_files(defn, cwd=None):
    for defn in yaml.safe_load_all(defn):
        build_one_file(defn, cwd)
