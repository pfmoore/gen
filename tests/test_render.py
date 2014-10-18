from gen.generate import build
from gen import renderer

def test_no_rendering(tmpdir):
    build('foo', content='$var {var} %(var)s', target=str(tmpdir))
    actual = (tmpdir / 'foo').read_text(encoding='utf-8')
    assert actual == '$var {var} %(var)s'

def test_template_rendering(tmpdir):
    var = {'var': 'bar'}
    build('foo', content='$var {var} %(var)s',
          renderer=renderer.stringtemplate_renderer,
          variables=var,
          target=str(tmpdir))
    actual = (tmpdir / 'foo').read_text(encoding='utf-8')
    assert actual == 'bar {var} %(var)s'

def test_percent_rendering(tmpdir):
    var = {'var': 'bar'}
    build('foo', content='$var {var} %(var)s',
          renderer=renderer.percent_renderer,
          variables=var,
          target=str(tmpdir))
    actual = (tmpdir / 'foo').read_text(encoding='utf-8')
    assert actual == '$var {var} bar'

def test_format_rendering(tmpdir):
    var = {'var': 'bar'}
    build('foo', content='$var {var} %(var)s',
          renderer=renderer.format_renderer,
          variables=var,
          target=str(tmpdir))
    actual = (tmpdir / 'foo').read_text(encoding='utf-8')
    assert actual == '$var bar %(var)s'
