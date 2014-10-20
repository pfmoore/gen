import yaml

def parse_yaml(filename):
    with open(filename, 'rb') as f:
        defn = yaml.load(f)

    ver = defn.get('version', 1)
    if ver != 1:
        raise ValueError('YAML file version is not compatible')

    files = defn.get('files', [])
    variables = defn.get('variables', [])

    # Work out how to do defaults later...
    return files, variables
