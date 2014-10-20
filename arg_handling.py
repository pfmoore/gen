import click

class ExtendedCommand(click.Command):
    allow_extra_args = True
    allow_interspersed_args=False
    ignore_unknown_options = True

def generate_command(defn, fn):
    params = [
        click.Option(['--' + name])
        for name in defn.split(':')
    ]
    cmd = click.Command('vars', callback=fn, params=params)
    return cmd

@click.command(cls=ExtendedCommand)
@click.argument("defn")
@click.pass_context
def main(ctx, defn):
    print("Main command executed:", defn)
    def fn(**kw):
        print("Main command handler:", kw)
    cmd = generate_command(defn, fn)
    print("Generated command:", ctx.args)
    cmd(ctx.args)

if __name__ == '__main__':
    main()
