from borax.htmls import HTMLString
from django_echarts.renders import render_widget, flat_chart

try:
    from domonic.dom import Element
except ImportError:
    raise TypeError('The domonic library is not installed yet? Use the command `pip install domonic`')


@render_widget.register(Element)
def render_dom(widget: Element, **kwargs):
    return HTMLString(widget.toString())


@flat_chart.register(Element)
def flat_for_html(widget):
    return []
