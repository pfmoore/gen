import click
from . import generate

@click.command()
@click.argument('template')
@click.option('--target', '-d', default='.',
        help="Render the template into this target directory (default: cwd)")
def main(template, target):
    "Generate files from TEMPLATE"
    with open(template) as f:
        defn = f.read()
    generate.build_files(defn, target)
