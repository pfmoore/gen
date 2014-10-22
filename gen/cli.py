import click

def variable_parser(variables, callback=None):
    options = []
    for var in variables:
        args = {}
        args['param_decls'] = ['--' + var['name']]
        if 'default' in var:
            args['default'] = var['default']
        options.append(click.Option(**args))
    cmd = click.Command('vars', callback=callback, params=options)
    return cmd
