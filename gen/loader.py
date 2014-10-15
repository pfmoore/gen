import os
import stat

class FilesystemLoader:
    def __init__(self, root):
        self.root = os.path.abspath(root)
    def list_templates(self):
        for dirpath, dirnames, filenames in os.walk(self.root):
            for name in filenames:
                yield os.path.relpath(os.path.join(dirpath, name), self.root)
    def get_source(self, name):
        path = os.path.join(self.root, name)
        with open(path, 'r') as f:
            return f.read()
    def get_executable(self, name):
        return (os.stat(os.path.join(self.root, name)).st_mode & stat.S_IXUSR) != 0
