import os
import click
from . import generate, loader

@click.command()
@click.argument('template')
@click.option('--target', '-d', default='.',
        help="Render the template into this target directory (default: cwd)")
def main(template, target):
    "Generate files from TEMPLATE"
    if os.path.isfile(template):
        with open(template) as f:
            defn = f.read()
        generate.build_files(defn, target)
    else:
        l = loader.FilesystemLoader(template)
        for name in l.list_templates():
            generate.build(name, content=l.get_source(name),
                           executable=l.get_executable(name), target=target)
