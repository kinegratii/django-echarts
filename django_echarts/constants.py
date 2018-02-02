# coding=utf8

TRANSPARENT = 'transparent'

COLOR_LIST = ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074',
              '#546570', '#c4ccd3']


class ChartType(object):
    LINE = 'line'
    BAR = 'bar'
    PIE = 'pie'
    SCATTER = 'scatter'
    EFFECT_SCATTER = 'effectScatter'
    RADAR = 'radar'
    TREE_MAP = 'treemap'
    BOX_PLOT = 'boxplot'
    CANDLESTICK = 'candlestick'
    HEAT_MAP = 'heatmap'
    MAP = 'map'
    PARALLEL = 'parallel'
    LINES = 'lines'
    GRAPH = 'graph'
    SANKEY = 'sankey'
    FUNNEL = 'funnel'
    GAUGE = 'gauge'
    PICTOR_BAR = 'pictorBar'
    THEME_RIVER = 'themeRiver'
    CUSTOM = 'custom'


class TitleTarget(object):
    SELF = 'self'
    BLANK = 'blank'


class FontStyle(object):
    NORMAL = 'normal'
    ITALIC = 'italic'
    OBLIQUE = 'oblique'


class FontWeight(object):
    NORMAL = 'normal'
    BOLD = 'bold'
    BOLDER = 'bolder'
    LIGHTER = 'lighter'


class BorderType(object):
    SOLID = 'solid'
    DASHED = 'dashed'
    DOTTED = 'dotted'


class Orient(object):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


class Position(object):
    TOP = 'top'
    BOTTOM = 'bottom'
    LEFT = 'left'
    RIGHT = 'right'


class AxisPointer(object):
    LINE = 'line'
    SHADOW = 'shadow'


class BrushToolBox(object):
    RECT = 'rect'
    POLYGON = 'polygon'
    LINE_X = 'lineX'
    LINE_Y = 'lineY'
    KEEP = 'keep'
    CLEAR = 'clear'


class ControlPosition(object):
    LEFT = 'left'
    RIGHT = 'right'


class ParallelLayout(object):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


class AxisType(object):
    VALUE = 'value'
    CATEGORY = 'category'
    TIME = 'time'
    LOG = 'log'


class GraphicType(object):
    GROUP = 'group'
    IMAGE = 'image'
    TEXT = 'text'
    RECT = 'rect'
    CIRCLE = 'circle'
    RING = 'ring'
    SECTOR = 'sector'
    ARC = 'arc'
    POLYGON = 'polygon'
    POLYLINE = 'polyline'
    LINE = 'line'
    BEZIER_CURVE = 'bezierCurve'


class SymbolType(object):
    CIRCLE = 'circle'
    RECT = 'rect'
    ROUND_RECT = 'roundRect'
    TRIANGLE = 'triangle'
    DIAMOND = 'diamond'
    PIN = 'pin'
    ARROW = 'arrow'


class TriggerOn(object):
    MOVE = 'mousemove'
    CLICK = 'click'
    MOVE_CLICK = 'mousemove|click'
    NONE = 'none'


class VisualMapType(object):
    CONTINUOUS = 'continuous'
    PIECEWISE = 'piecewise'


class DataZoomType(object):
    INSIDE = 'inside'
    SLIDER = 'slider'
