import os
import json
import stat
from collections import OrderedDict

try:
    from binaryornot.check import is_binary
except ImportError:
    # We don't have binaryornot - assume all files are text
    def is_binary(filename):
        return False

def spec_from_cookiecutter(dirname):
    template = os.path.join(dirname, '{{cookiecutter.repo_name}}')
    jsonfile = os.path.join(dirname, 'cookiecutter.json')

    if not (os.path.exists(template) and os.path.exists(jsonfile)):
        raise ValueError("{} is not a valid Cookiecutter".format(dirname))

    variables = []
    with open(jsonfile) as j:
        vardata = json.load(j, object_pairs_hook=OrderedDict)
    for name, default in vardata.items():
        variables.append({'name': name, 'default': default})

    specs = []
    for dirpath, dirnames, filenames in os.walk(template):
        basepath = dirpath[len(dirname):]
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            spec = {}
            name = os.path.join(basepath, filename)
            spec['name'] = name
            binary_file = is_binary(fullpath)
            if not binary_file:
                try:
                    # Do we want to explicitly choose UTF-8?
                    with open(fullpath) as f:
                        # Read the data first, so we get an error for binary files
                        # before we set encoding or renderer
                        spec['content'] = f.read()
                        spec['encoding'] = f.encoding
                        spec['renderer'] = 'jinja2'
                except UnicodeDecodeError:
                    binary_file = True
            if binary_file:
                with open(fullpath, 'rb') as f:
                    spec['content'] = f.read()
                    spec['binary'] = True
            if (os.stat(fullpath).st_mode & stat.S_IXUSR) != 0:
                spec['executable'] = True
            specs.append(spec)

    return specs, variables

if __name__ == '__main__':
    import sys
    from pprint import pprint
    specs, variables = spec_from_cookiecutter(sys.argv[1])
    pprint(specs)
    pprint(variables)
