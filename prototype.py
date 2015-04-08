import click

def make_template_command(name):
    return click.Command(name)

class TemplateCommands(click.MultiCommand):
    def list_commands(self, ctx):
        return ['foo', 'bar']
    def get_command(self, ctx, name):
        return make_template_command(name)

@click.group(cls=TemplateCommands, help="Generate source files from templates",
             invoke_without_command=True)
@click.option('--list-templates', is_flag=True, help="List available templates")
@click.pass_context
def cli(ctx, list_templates):
    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand')
        if list_templates:
            click.echo("Commands: " + ', '.join(ctx.command.list_commands(ctx)))
    else:
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)


if __name__ == '__main__':
    cli()
