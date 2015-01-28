import os
import io
import stat

# A build spec is a dictionary, with the following keys:
#
# name (mandatory, string):
#   The name of the file to create
# name_renderer (optional, string or callable):
#   The name of the renderer to use for the filename (default, copy as is)
#   A callable can be supplied which will be used directly (no name lookup)
# directory (optional, boolean):
#   Create a directory rather than a file
#   If the filename ends with os.pathsep, it's treated as if this was set
#   Takes precedence over any content specification
# content (optional, string or bytes):
#   The content of the file (default, an empty file)
#   May be a Unicode string or a bytes object
#   The content will be written as text if it is a string, or binary if bytes
# binary (optional, boolean):
#   The content should be treated as binary (default, assume text)
#   An error will be raised if this is set and content is a Unicode string
#   (type unicode in Python 2, type str in Python 3)
# renderer (optional, string or callable):
#   The name of the renderer to use for the content (default, copy as is)
#   A callable can be supplied which will be used directly (no name lookup)
#   This will be ignored if the binary flag is set
#   TODO: Does rendering binary content make sense? Should it be allowed?
# encoding (optional, string):
#   The encoding the file will be written in (default, the filesystem encoding)
#   TODO: Maybe the default should be utf-8?
#   This will be ignored if the binary flag is set
# executable (optional, boolean):
#   The executable flag will be set on the file (default, don't set it)
#
# Under Python 2, it is not possible to detect that an argument is a bytes
# object rather than a string, so in practice the binary flag should always
# be set explicitly, to avoid subtle errors.

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

# Allow unknown keys for future expansion, so don't check this
# spec_keys = {
#     'name',
#     'name_renderer',
#     'directory',
#     'content',
#     'binary',
#     'renderer',
#     'encoding',
#     'executable',
# }

def build(spec, variables=None, target=None):
    # Look up a renderer by name
    def get_renderer(renderer):
        renderer = spec.get(renderer)
        if renderer and not callable(renderer):
            try:
                renderer = renderers[renderer]
            except KeyError:
                raise ValueError("Invalid renderer name '{}'".format(renderer))
        return renderer

    # Make sure we have a filename
    if 'name' not in spec:
        raise ValueError("Spec must have a 'name' element")
    filename = spec['name']

    # Render the filename if needed, and make it relative to the target
    name_renderer = get_renderer('name_renderer')
    if name_renderer:
        filename = name_renderer(filename, variables)
    if target:
        # TODO: Potential security risk, if filename is absolute this
        # could create a file outside of the target directory
        filename = os.path.join(target, filename)

    # Create any parent directories needed
    dirname, basename = os.path.split(filename)
    ensuredir(dirname)

    # If the filename ends with os.sep, or directory is set,
    # create the final directory if needed, and stop
    if not basename:
        return
    if spec.get('directory'):
        os.mkdir(filename)
        return

    # We are creating a file
    # Open as binary, as we will do our own encoding
    with open(filename, 'wb') as f:
        content = spec.get('content')
        if content:
            if 'binary' in spec:
                binary = spec['binary']
            else:
                # If it's bytes treat it as binary unless it's also a str,
                # in which case we're Python 2 and we should assume the
                # intent is text.
                binary = (isinstance(spec, bytes) and not isinstance(spec, str))
            if not binary:
                renderer = get_renderer('renderer')
                if renderer:
                    content = renderer(content, variables)
                encoding = spec.get('encoding', 'utf-8')
                # Always encode, as content is a string and needs to be bytes
                content = content.encode(encoding)
            f.write(content)

    # Do we need to make the file executable?
    if spec.get('executable'):
        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR)
