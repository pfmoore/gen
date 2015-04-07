import click
import yaml
from gen.generate import build

def foo(*args, **kw):
    print("FOO", args, kw)

class MyCLI(click.MultiCommand):

    def load(self, filename='examples.yml'):
        with open(filename, 'rb') as f:
            self.defns = list(yaml.load_all(f))

    def list_commands(self, ctx):
        return [d['name'] for d in self.defns]

    def get_command(self, ctx, name):
        defn = [d for d in self.defns if d['name'] == name][0]
        variables = defn['variables']
        params=[click.Option(['--'+v], str) for v in variables]
        def build_cmd(**variables):
            for spec in defn['definition']:
                build(spec, variables, target='xx')

        cmd = click.Command(name, params=params, callback=build_cmd)
        return cmd

cli = MyCLI(help="Example")
cli.load()

if __name__ == '__main__':
    cli()
