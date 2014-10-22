import os
import io
import stat
import yaml

from .renderer import renderers

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

# TODO: Make a builder class, that has target, renderer, name renderer and
# encoding as attributes?
def build(filename, content=None, directory=False, encoding='utf-8',
          executable=False, target=None, renderer=None, variables=None):
    # TODO: render filename and content independently?
    if not callable(renderer):
        renderer = renderers.get(renderer)
    if renderer:
        filename = renderer(filename, variables)
    if target:
        filename = os.path.join(target, filename)
    dirname, basename = os.path.split(filename)
    ensuredir(dirname)
    if not basename:
        return
    if directory:
        os.mkdir(filename)
        return
    with open(filename, 'wb') as f:
        if content:
            if renderer:
                content = renderer(content, variables)
            # TODO: encode before or after rendering?
            if encoding:
                content = content.encode(encoding)
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
