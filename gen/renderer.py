from string import Template

def format_renderer(content, variables):
    return content.format_map(variables)

def stringtemplate_renderer(content, variables):
    t = Template(content)
    return t.safe_substitute(variables)

def percent_renderer(content, variables):
    return content % variables

renderers = {
    'format': format_renderer,
    'stringtemplate': stringtemplate_renderer,
    'percent': percent_renderer,
}

def deregister_renderer(name, renderer):
    del renderers[name]

def register_renderer(name, renderer):
    renderers[name] = renderer

try:
    import jinja2
except ImportError:
    jinja2 = None

if jinja2:
    def jinja2_renderer(content, variables):
        t = jinja2.Template(content)
        return t.render(variables)

    register_renderer('jinja2', jinja2_renderer)
