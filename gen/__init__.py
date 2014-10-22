import os
import click
from . import generate, loader, parser, cli

__version__ = '0.2.dev1'

def build(defn, target, variables):
    filename = defn.pop('name')
    generate.build(filename=filename, target=target, variables=variables, **defn)

class ExtendedCommand(click.Command):
    allow_extra_args = True
    allow_interspersed_args=False
    ignore_unknown_options = True

@click.command(cls=ExtendedCommand)
@click.argument('template')
@click.option('--target', '-d', default='.',
        help="Render the template into this target directory (default: cwd)")
@click.version_option(version=__version__)
@click.pass_context
def main(ctx, template, target):
    "Generate files from TEMPLATE"
    if os.path.isfile(template):
        files, variables = parser.parse_yaml(template)
        def callback(**kw):
            for f in files:
                build(f, target, kw)
        cmd = cli.variable_parser(variables, callback)
        cmd(ctx.args)
    else:
        l = loader.FilesystemLoader(template)
        for name in l.list_templates():
            generate.build(name, content=l.get_source(name),
                           executable=l.get_executable(name), target=target)
