import json
from dataclasses import dataclass
from functools import wraps
from typing import Optional, List, Dict, Callable, Literal, Type, Any

from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.urls import reverse_lazy, path
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

from django_echarts.core.charttools import DJEChartInfo, LocalChartManager, ChartManagerMixin
from django_echarts.core.exceptions import DJEAbortException
from django_echarts.core.themes import get_theme, Theme
from django_echarts.utils.compat import get_elided_page_range
from .widgets import Nav, LinkItem, Jumbotron, Copyright

__all__ = ['DJESite', 'SiteOpts', 'ttn', 'DJESiteBaseView']


def ttn(template_name: str, theme: str = None) -> str:
    """Resolve for theme template name."""
    theme_template_name = template_name
    if template_name and template_name[:7] != '{theme}':
        theme_template_name = '{theme}/' + template_name
    if not theme:
        return theme_template_name
    else:
        return theme_template_name.format(theme=theme)


class DJESiteBaseView(TemplateResponseMixin, ContextMixin, View):
    """The base view for Site.
    """

    def get(self, request, *args, **kwargs):
        site = DJESiteBaseView.get_site_object()
        context = self.get_context_data(site=site, **kwargs)
        try:
            template_name = self.dje_init_page_context(context=context, site=site)
            if isinstance(template_name, dict):
                raise TypeError(
                    'The method dje_init_page_context should return a string for template name.Not a dict for context.')
        except DJEAbortException as e:
            context['message'] = e.message
            template_name = ttn('message.html')
        theme_name = context['theme'].name
        return self._render_to_response(context, theme_name=theme_name, template_name=template_name)

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
        return template_name.format(theme=self.extra_context['theme'].name)

    @staticmethod
    def get_site_object(site: 'DJESite' = None):
        return site

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = kwargs.get('site')  # type: DJESite
        context['nav'] = site.nav
        context['site_title'] = site.site_title
        context['page_title'] = site.site_title
        context['copyright'] = site.widgets.get('copyright')
        # select a theme
        theme = site.dje_get_current_theme(self.request)
        context['theme'] = theme
        context['opts'] = site.opts

        # The data store in a view processing lifecycle.
        self.extra_context = {
            'theme': theme
        }
        return context

    # Interfaces

    def abort_request(self, message: str):
        """Abort current request and show the message page."""
        raise DJEAbortException(message)

    def dje_get_template_name(self, theme_name, template_name: str = None):
        template_name = template_name or self.template_name
        return template_name.format(theme=theme_name)

    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        """Update context and return its template name.
        If no template name returned, use the value returned by self.dje_get_template_name
        """
        pass


class DJESiteDetailBaseView(DJESiteBaseView):
    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        chart_name = self.kwargs.get('name')
        chart_info = site.chart_manager.get_or_none(chart_name)
        context['chart_info'] = chart_info
        if not chart_info:
            self.abort_request('The chart does not exist.')
        return self.template_name


class DJESiteAjaxView(View):
    """The helper view class for ajax request."""

    def get(self, request, *args, **kwargs):
        site = DJESiteAjaxView.get_site_object()
        data = self.dje_get(request, site=site, *args, **kwargs)
        if isinstance(data, JsonResponse):
            return data
        else:
            return JsonResponse(data, safe=False)

    def post(self, request, *args, **kwargs):
        site = DJESiteAjaxView.get_site_object()
        data = self.dje_post(request, site=site, *args, **kwargs)
        if isinstance(data, JsonResponse):
            return data
        else:
            return JsonResponse(data, safe=False)

    def dje_get(self, request, *args, **kwargs) -> Any:
        pass

    def dje_post(self, request, *args, **kwargs) -> Any:
        pass

    @staticmethod
    def get_site_object(site: 'DJESite' = None):
        return site


# The Page Views

class DJESiteHomeView(DJESiteBaseView):
    template_name = ttn('home.html')

    def dje_init_page_context(self, context, site: 'DJESite'):
        context['jumbotron'] = site.widgets.get('jumbotron')
        context['top_chart_info_list'] = site.chart_manager.query_chart_info_list(with_top=True)
        context['layout_tpl'] = self._resolve_template_name('{theme}/items_grid.html')


class DJESiteListView(DJESiteBaseView):
    template_name = ttn('list.html')
    paginate_by = None
    list_layout = 'list'
    page_kwarg = 'page'
    query_kwarg = 'query'

    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        theme = context['theme']
        if site.opts.list_layout == 'grid':
            layout_tpl = ttn('items_grid.html', theme.name)
        else:
            layout_tpl = ttn('items_list.html', theme.name)
        context['layout_tpl'] = layout_tpl
        query_string = self.request.GET.get(self.query_kwarg)
        qs = {}
        if query_string:
            qs.update({'keyword': query_string})
            context['keyword'] = query_string
        chart_info_list = site.chart_manager.query_chart_info_list(**qs)
        paginate_by = site.opts.paginate_by
        if paginate_by is None:
            context['chart_info_list'] = chart_info_list
            return ttn('list.html')
        else:
            paginator = Paginator(chart_info_list, paginate_by, allow_empty_first_page=True)
            page_number = self.request.GET.get(self.page_kwarg, 1)
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
            try:
                # Django3.2+
                elided_page_nums = paginator.get_elided_page_range(page_number)
            except (AttributeError, TypeError, ValueError):
                elided_page_nums = get_elided_page_range(paginator, page_number)
            context['elided_page_nums'] = list(elided_page_nums)
            return ttn('list_with_paginator.html')


class DJESiteDetailView(DJESiteBaseView):
    template_name = ttn('detail.html')

    charts_config = []
    page_title = '{title}'

    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        context['view_name'] = 'dje_detail'
        chart_name = self.kwargs.get('name')
        found = False
        menu_text = None
        info_list = site.chart_manager.query_chart_info_list()
        for info in info_list:
            if chart_name == info.name and not found:
                found = True
                menu_text = info.parent_name
                func = site.get_chart_func(chart_name)
                chart_obj = None
                if func:
                    chart_obj = func()
                if chart_obj:
                    chart_obj.width = '100%'
                    context['chart_info'] = info
                    context['chart_obj'] = chart_obj
                    context['title'] = self.get_dje_page_title(name=info.name, title=info.title)
                selected = True
            else:
                selected = False
            info.selected = selected
        if menu_text:
            context['menu'] = [info for info in info_list if info.parent_name == menu_text]
        if found:
            return self.template_name
        else:
            self.abort_request('The chart does not exist.')

    def get_dje_page_title(self, name, title, **kwargs):
        return self.page_title.format(name=name, title=title)


class DJSiteChartOptionsView(DJESiteAjaxView):
    def dje_get(self, request, *args, **kwargs) -> Any:
        chart_name = self.kwargs.get('name')
        site = DJESiteAjaxView.get_site_object()
        func = site.get_chart_func(chart_name)
        if not func:
            return {}
        else:
            chart_obj = func()
            return json.loads(chart_obj.dump_options_with_quotes())


class DJESiteAboutView(DJESiteBaseView):
    template_name = ttn('about.html')


@dataclass
class SiteOpts:
    """The opts for DJESite."""
    list_nav_item_shown: bool = True
    list_layout: Literal['grid', 'list'] = 'list'
    paginate_by: Optional[int] = None
    detail_tags_position: Literal['none', 'top', 'bottom'] = 'top'
    detail_sidebar_shown: bool = True


class DJESite:
    """A generator endpoint for visual chart site.
    Example:
        site_obj = DJESite(site_title='MySite', opts=SiteOpts(paginate_by=10))
    """

    chart_manager_class = LocalChartManager  # type: Type[ChartManagerMixin]

    def __init__(self, site_title: str = 'My Charts Demo', theme: str = 'bootstrap3',
                 opts: Optional[SiteOpts] = None):
        self.site_title = site_title
        self.theme = get_theme(theme)
        if opts is None:
            self._opts = SiteOpts()
        else:
            self._opts = opts
        self.nav = Nav()
        self.nav.add_menu(text='首页', slug='home', url=reverse_lazy('dje_home'))
        if self._opts.list_nav_item_shown:
            self.nav.add_menu(text='All', slug='list', url=reverse_lazy('dje_list'))
        self.widgets = {}
        self._view_dict = {
            'home': DJESiteHomeView,
            'detail': DJESiteDetailView,
            'chart_options': DJSiteChartOptionsView,
            'list': DJESiteListView,
            'about': DJESiteAboutView
        }
        # Inject site object to views.
        DJESiteBaseView.get_site_object = self._inject(DJESiteBaseView.get_site_object)
        DJESiteAjaxView.get_site_object = self._inject(DJESiteAjaxView.get_site_object)

        # Charts

        self._chart_name2func = {}  # type: Dict[str,Callable]
        self._chart_manager = self.chart_manager_class()  # type: ChartManagerMixin

    def _inject(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            selected_deps = {'site': self}
            new_kwargs = {**kwargs, **selected_deps}
            return func(*args, **new_kwargs)

        return decorated

    @property
    def opts(self) -> SiteOpts:
        return self._opts

    @property
    def chart_manager(self) -> ChartManagerMixin:
        return self._chart_manager

    # Init Widgets
    def add_menu_item(self, item: LinkItem, menu_title: str = None):
        self.nav.add_item(menu_text=menu_title, item=item)
        return self

    def add_link(self, item: LinkItem):
        """Add link on nav."""
        self.nav.add_right_link(item)
        return self

    def add_widgets(self, *, jumbotron: Jumbotron = None, copyright_: Copyright = None):
        """Add widgets to the site."""
        if jumbotron:
            self.widgets['jumbotron'] = jumbotron
        if copyright_:
            self.widgets['copyright'] = copyright_
        return self

    # Register function and views class
    def register_chart(self, function=None, *, info: DJEChartInfo = None, name: str = None, title: str = None,
                       description: str = None, top: int = 0, catalog: str = None, tags: List = None,
                       after_separator: bool = False):
        """Register chart function."""

        # TODO Add support lru_cache
        def decorator(func):
            cname = name or func.__name__
            url = reverse_lazy('dje_detail', args=(cname,))
            if info:
                cinfo = info
            else:
                cinfo = DJEChartInfo(name=cname, title=title or cname, description=description,
                                     url=url, top=top, parent_name=catalog, tags=tags)
            self._chart_name2func[cinfo.name] = func
            self._chart_manager.add_chart_info(cinfo)
            if catalog:
                self.nav.add_menu(text=catalog)
                self.nav.add_item(
                    menu_text=catalog,
                    item=LinkItem(text=title or cname, url=url, slug=cname),
                    after_separator=after_separator
                )
            return func

        if function is None:
            return decorator
        else:
            return decorator(function)

    # The function api for accessing site data.

    def get_chart_func(self, name: str) -> Optional[Callable]:
        return self._chart_name2func.get(name)

    @property
    def urls(self):
        """Return the URLPattern list for site entrypoint."""
        urls = [
            path('', self._view_dict['home'].as_view(), name='dje_home'),
            path('list/', self._view_dict['list'].as_view(), name='dje_list'),
            path('chart/<slug:name>/', self._view_dict['detail'].as_view(), name='dje_detail'),
            path('chart/<slug:name>/options/', self._view_dict['chart_options'].as_view(), name='dje_chart_options'),
            path('about/', self._view_dict['about'].as_view(), name='dje_about')
        ]
        custom_url = self.dje_get_urls()
        if custom_url:
            urls += custom_url
        return urls

    # Public Interfaces

    def dje_get_current_theme(self, request, *args, **kwargs) -> Theme:
        """Get the theme for this request."""
        return self.theme

    def dje_get_urls(self) -> List:
        """Custom you url routes here."""
        pass
