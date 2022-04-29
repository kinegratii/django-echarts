from borax.htmls import HTMLString
from django_echarts.renders import render_widget, flat_chart

try:
    from yattag.doc import Doc
except ImportError:
    raise TypeError('The yattag library is not installed yet? Use the command `pip install yattag`')


@render_widget.register(Doc)
def render_dom(widget: Doc, **kwargs):
    return HTMLString(widget.getvalue())


@flat_chart.register(Doc)
def flat_for_html(widget):
    return []
