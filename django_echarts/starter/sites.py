from functools import wraps
from typing import Type, Union, Optional, List, Dict, Callable, Literal

from django.core.paginator import Paginator
from django.urls import reverse_lazy, path
from django.views.generic.base import TemplateView

from django_echarts.dms.themes import get_theme
from .widgets import Nav, LinkItem, Jumbotron, Copyright

__all__ = ['DJESite', 'DJESiteHomeView', 'DJESiteDetailView', 'DJESiteListView', 'ttn']


class DJEChartInfo:
    __slots__ = ['name', 'title', 'description', 'url', 'selected', 'parent_name', 'top']

    def __init__(self, name: str, title: str = None, description: str = None, url: str = None,
                 selected: bool = False, parent_name: str = None, top: int = 0):
        self.name = name
        self.title = title or self.name
        self.description = description or ''
        self.url = url
        self.selected = selected
        self.top = top
        self.parent_name = parent_name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f'<ChartInfo {self.name}>'


def ttn(template_name: str) -> str:
    """Resolve for theme template name."""
    theme_template_name = template_name
    if template_name and template_name[:7] != '{theme}':
        theme_template_name = '{theme}' + template_name
    return theme_template_name


class DJESiteBaseView(TemplateView):
    """The base view for Site.
    """

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        site = DJESiteBaseView.get_site_object()
        template_name = self.dje_init_page_context(context=context, site=site)
        return self._render_to_response(context, theme_name=context['theme_name'], template_name=template_name)

    def _render_to_response(self, context, template_name=None, **kwargs):
        template_name = self._resolve_template_name(template_name)
        return self.response_class(
            request=self.request,
            template=template_name,
            context=context,
            using=self.template_engine
        )

    def _resolve_template_name(self, template_name: str = None):
        if template_name and template_name[:7] != '{theme}':
            template_name = '{theme}' + template_name
        template_name = template_name or self.template_name
        return template_name.format(theme=self.extra_context['theme_name'])

    @staticmethod
    def get_site_object(site: 'DJESite' = None):
        return site

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = DJESiteBaseView.get_site_object()
        context['nav'] = site.nav
        context['site_title'] = site.site_title
        context['copyright'] = site.widgets.get('copyright')
        context['theme'] = site.theme
        context['theme_name'] = site.theme.name

        # The data store in a view processing lifecycle.
        self.extra_context = {
            'theme_name': site.theme.name
        }
        return context

    # Interfaces

    def dje_get_template_name(self, theme_name, template_name: str = None):
        template_name = template_name or self.template_name
        return template_name.format(theme=theme_name)

    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        """Update context and return its template name.
        If no template name returned, use the value returned by self.dje_get_template_name
        """
        pass


class DJESiteHomeView(DJESiteBaseView):
    template_name = '{theme}/home.html'

    def dje_init_page_context(self, context, site: 'DJESite'):
        context['jumbotron'] = site.widgets.get('jumbotron')
        context['top_chart_list'] = site.get_chart_info_list(with_top=True)
        context['layout_tpl'] = self._resolve_template_name('{theme}/items_grid.html')


class DJESiteListView(DJESiteBaseView):
    template_name = '{theme}/list.html'
    paginate_by = None
    list_layout = 'list'

    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        chart_list = site.get_chart_info_list()
        paginate_by = site.get_opt('paginate_by')
        if self.list_layout == 'grid':
            layout_tpl = '{theme}/items_grid.html'.format(theme=site.theme.name)
        else:
            layout_tpl = '{theme}/items_list.html'.format(theme=site.theme.name)
        context['layout_tpl'] = layout_tpl
        if paginate_by is None:
            context['chart_list'] = chart_list
            return '{theme}/list.html'
        else:
            paginator = Paginator(chart_list, paginate_by, allow_empty_first_page=True)
            page_number = self.request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
            try:
                # Django3.2+
                elided_page_nums = paginator.get_elided_page_range(page_number)
                context['elided_page_nums'] = list(elided_page_nums)
            except (AttributeError, TypeError, ValueError):
                pass
            return '{theme}/list_with_paginator.html'


class DJESiteDetailView(DJESiteBaseView):
    template_name = '{theme}/detail.html'
    empty_template_name = '{theme}/empty.html'

    charts_config = []
    page_title = '{title}'

    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        context['view_name'] = 'dje_detail'
        chart_name = self.kwargs.get('name')
        found = False
        menu_text = None
        info_list = site.get_chart_info_list()
        for info in info_list:
            if chart_name == info.name and not found:
                found = True
                menu_text = info.parent_name
                func = getattr(self, f'dje_chart_{chart_name}', None)
                chart_obj = None
                if func:
                    chart_obj = func()
                else:
                    func = site.get_chart_func(chart_name)
                    if func:
                        chart_obj = func()
                if chart_obj:
                    context['chart_obj'] = chart_obj
                    context['title'] = self.get_dje_page_title(name=info.name, title=info.title)
                selected = True
            else:
                selected = False
            info.selected = selected
        if menu_text:
            context['menu'] = [info for info in info_list if info.parent_name == menu_text]
        if found:
            tpl = self.template_name
        else:
            tpl = self.empty_template_name
        return tpl

    def get_dje_page_title(self, name, title, **kwargs):
        return self.page_title.format(name=name, title=title)


class DJESiteAboutView(DJESiteBaseView):
    template_name = '{theme}/about.html'


class DJESite:
    """A generator endpoint for visual chart site."""

    def __init__(self, site_title: str = 'My Charts Demo', theme: str = 'bootstrap3', copyright_: Copyright = None,
                 list_page_shown: bool = True, paginate_by: Optional[int] = None,
                 list_layout: Literal['grid', 'list'] = 'list'):
        self.site_title = site_title
        self.theme = get_theme(theme.split('.')[0], theme)
        self.nav = Nav()
        self.nav.add_menu(text='首页', slug='home', url=reverse_lazy('dje_home'))
        if list_page_shown:
            self.nav.add_menu(text='列表', slug='list', url=reverse_lazy('dje_list'))
        self.widgets = {}
        if copyright_:
            self.widgets['copyright'] = copyright_
        self._opts = {
            'paginate_by': paginate_by,
            'list_layout': list_layout
        }

        self._view_dict = {
            'home': DJESiteHomeView,
            'detail': DJESiteDetailView,
            'list': DJESiteListView,
            'about': DJESiteAboutView
        }

        DJESiteBaseView.get_site_object = self._inject(DJESiteBaseView.get_site_object)

        self._charts = dict()  # type: Dict[DJEChartInfo,Optional[Callable]]

    def _inject(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            selected_deps = {'site': self}
            new_kwargs = {**kwargs, **selected_deps}
            return func(*args, **new_kwargs)

        return decorated

    # Init Widgets
    def add_menu_item(self, item: LinkItem, menu_title: str = None):
        self.nav.add_item(menu_text=menu_title, item=item)

    def add_link(self, item: LinkItem):
        self.nav.add_right_link(item)
        return self

    def add_widgets(self, *widgets: Union[Jumbotron, Copyright]):
        for widget in widgets:
            self.widgets[widget.__class__.__name__.lower()] = widget
        return self

    # Register function and views class
    def register_chart(self, function=None, name: str = None, title: str = None, description: str = None,
                       top: int = 0, menu_text: str = None):
        """Register chart function."""

        def decorator(func):
            cname = name or func.__name__
            url = reverse_lazy('dje_detail', args=(cname,))
            info = DJEChartInfo(name=cname, title=title or cname, description=description,
                                url=url, top=top, parent_name=menu_text)
            self._charts[info] = func  # TODO check method/function
            if menu_text:
                self.nav.add_menu(text=menu_text)
                self.nav.add_item(
                    menu_text=menu_text,
                    item=LinkItem(text=title or cname, url=url, slug=cname)
                )
            return func

        if function is None:
            return decorator
        else:
            return decorator(function)

    def register_home_view(self, view_class: Type[DJESiteHomeView], ):
        """Register custom view class for home page."""
        self._view_dict['home'] = view_class
        return self

    def register_list_view(self, view_class: Type[DJESiteListView]):
        """Register custom view class for list page."""
        self._view_dict['list'] = view_class
        if view_class.paginate_by:
            self._opts['paginate_by'] = view_class.paginate_by
        return self

    def register_detail_view(self, view_class: Type[DJESiteDetailView], menu_text: str = None):
        """Register custom view class for detail page."""
        self._view_dict['detail'] = view_class
        self.nav.add_menu(text=menu_text)
        for _name, _title in view_class.charts_config:
            url = reverse_lazy('dje_detail', args=(_name,))
            self.nav.add_item(
                menu_text=menu_text,
                item=LinkItem(text=_title, url=reverse_lazy('dje_detail', args=(_name,)), slug=_name)
            )
            info = DJEChartInfo(name=_name, title=_title, url=url, parent_name=menu_text)
            self._charts[info] = None
        return self

    # The function api for accessing site data.

    def get_opt(self, key: str, default=None):
        return self._opts.get(key, default)

    def get_chart_info_list(self, with_top: bool = False) -> List[DJEChartInfo]:
        chart_info_list = [info for info in self._charts.keys() if not with_top or info.top]
        if with_top:
            chart_info_list.sort(key=lambda x: x.top)
        return chart_info_list

    def get_chart_func(self, name: str) -> Optional[Callable]:
        for chart_info, func in self._charts.items():
            if chart_info.name == name:
                return func

    @property
    def urls(self):
        """Return the URLPattern list for site entrypoint."""
        return [
            path('', self._view_dict['home'].as_view(), name='dje_home'),
            path('list/', self._view_dict['list'].as_view(), name='dje_list'),
            path('detail/<slug:name>/', self._view_dict['detail'].as_view(), name='dje_detail'),
            path('about/', self._view_dict['about'].as_view(), name='dje_about')
        ]
