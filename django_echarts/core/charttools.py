class DJEChartInfo:
    """The meta-data class for a chart."""
    __slots__ = ['name', 'title', 'description', 'url', 'selected', 'parent_name', 'top', 'tags']

    def __init__(self, name: str, title: str = None, description: str = None, url: str = None,
                 selected: bool = False, parent_name: str = None, top: int = 0, tags=None):
        self.name = name
        self.title = title or self.name
        self.description = description or ''
        self.url = url
        self.selected = selected
        self.top = top
        self.parent_name = parent_name
        self.tags = tags or []

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f'<ChartInfo {self.name}>'
