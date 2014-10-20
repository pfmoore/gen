import os
import click
from . import generate, loader, parser

__version__ = '0.2.dev1'

def build(defn, target, variables):
    filename = defn.pop('name')
    generate.build(filename=filename, target=target, variables=variables, **defn)

@click.command()
@click.argument('template')
@click.option('--target', '-d', default='.',
        help="Render the template into this target directory (default: cwd)")
@click.version_option(version=__version__)
def main(template, target):
    "Generate files from TEMPLATE"
    if os.path.isfile(template):
        files, variables = parser.parse_yaml(template)
        # Work out how to do variables later
        for f in files:
            build(f, target, variables)
    else:
        l = loader.FilesystemLoader(template)
        for name in l.list_templates():
            generate.build(name, content=l.get_source(name),
                           executable=l.get_executable(name), target=target)
