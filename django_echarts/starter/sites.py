import json
import pprint
import re
from dataclasses import dataclass, field
from functools import wraps
from typing import Optional, List, Dict, Literal, Type, Any, Tuple, Union

from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.urls import reverse_lazy, path
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django_echarts.core.exceptions import DJEAbortException
from django_echarts.core.themes import get_theme, Theme
from django_echarts.entities.articles import ChartInfo, LocalChartInfoManager, ChartInfoManagerMixin
from django_echarts.entities.charttools import WidgetGetterMixin, WidgetCollection
from django_echarts.entities.widgets import Nav, LinkItem, Jumbotron, Copyright, Message, ValuesPanel
from django_echarts.utils.compat import get_elided_page_range
from django_echarts.utils.lazy_dict import LazyDict

__all__ = ['DJESite', 'SiteOpts', 'ttn', 'DJESiteBackendView']

_VAR_CHART_ = 'chart_obj'
_VAR_CHART_INFO_ = 'chart_info'
_VAR_PAGE_CONTAINER_ = 'chart_page_container'


class WidgetRefs:
    """Used for context variable names."""
    home_jumbotron = 'home_jumbotron'
    home_jumbotron_chart = 'home_jumbotron_chart'
    home_values_panel = 'home_values_panel'


def ttn(template_name: str, theme_name: str = None) -> str:
    """Resolve for theme template name."""
    theme_template_name = template_name
    if template_name and template_name[:7] != '{theme}':
        theme_template_name = '{theme}/' + template_name
    if not theme_name:
        return theme_template_name
    else:
        return theme_template_name.format(theme=theme_name)


class SiteInjectMixin:
    @staticmethod
    def get_site_object(site: 'DJESite' = None):
        return site


class DJESiteBackendView(TemplateResponseMixin, ContextMixin, SiteInjectMixin, View):
    """The base view for Site.
    """

    def get(self, request, *args, **kwargs):
        site = SiteInjectMixin.get_site_object()
        context = self.get_context_data(site=site, **kwargs)
        try:
            template_name = self.dje_init_page_context(context=context, site=site)
            if isinstance(template_name, dict):
                raise TypeError(
                    'The method dje_init_page_context should return a string for template name.Not a dict for context.')
        except DJEAbortException as e:
            context['message'] = Message(e.message, catalog='warning')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = kwargs.get('site')  # type: DJESite
        context['nav'] = site.nav
        context['site_title'] = site.site_title
        context['page_title'] = site.site_title
        context['copyright'] = site.html_widgets.get('copyright')
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


class DJESiteDetailBaseView(DJESiteBackendView):
    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        chart_name = self.kwargs.get('name')
        chart_info = site.chart_info_manager.get_or_none(chart_name)
        context['chart_info'] = chart_info
        if not chart_info:
            self.abort_request('The chart does not exist.')
        return self.template_name


class DJESiteCollectionView(DJESiteBackendView):
    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        collection_name = self.kwargs.get('name', 'all')
        # TODO entry
        widget_collection = site.build_collection(collection_name)
        pprint.pprint(widget_collection.packed_matrix)
        context[_VAR_PAGE_CONTAINER_] = widget_collection
        return ttn('chart_collection.html')


class DJESiteFrontendView(SiteInjectMixin, View):
    """The helper view class for ajax request."""

    def get(self, request, *args, **kwargs):
        site = SiteInjectMixin.get_site_object()
        data = self.dje_get(request, site=site, *args, **kwargs)
        if isinstance(data, JsonResponse):
            return data
        else:
            return JsonResponse(data, safe=False)

    def post(self, request, *args, **kwargs):
        site = SiteInjectMixin.get_site_object()
        data = self.dje_post(request, site=site, *args, **kwargs)
        if isinstance(data, JsonResponse):
            return data
        else:
            return JsonResponse(data, safe=False)

    def dje_get(self, request, *args, **kwargs) -> Any:
        pass

    def dje_post(self, request, *args, **kwargs) -> Any:
        pass


# The Page Views

class DJESiteHomeView(DJESiteBackendView):
    template_name = ttn('home.html')

    def dje_init_page_context(self, context, site: 'DJESite'):
        context['jumbotron'] = site.html_widgets.get(WidgetRefs.home_jumbotron)
        chart_obj, _, info = site.resolve_chart(WidgetRefs.home_jumbotron_chart)
        if chart_obj:
            context[_VAR_CHART_] = chart_obj
            context[_VAR_CHART_INFO_] = info
        context[WidgetRefs.home_values_panel] = site.html_widgets.get(WidgetRefs.home_values_panel)
        context['top_chart_info_list'] = site.chart_info_manager.query_chart_info_list(with_top=True)
        context['layout_tpl'] = self._resolve_template_name('{theme}/items_grid.html')


class DJESiteListView(DJESiteBackendView):
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
        chart_info_list = site.chart_info_manager.query_chart_info_list(**qs)
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


class DJESiteChartSingleView(DJESiteBackendView):
    template_name = ttn('chart_single.html')

    charts_config = []
    page_title = '{title}'

    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        context['view_name'] = 'dje_chart_single'
        chart_name = self.kwargs.get('name')
        chart_obj, func_exists, chart_info = site.resolve_chart(chart_name)
        if not func_exists:
            self.abort_request('The chart does not exist.')
        if not chart_obj:
            self.abort_request(f'The chart function {chart_name} returns nothing..')
        chart_obj.width = '100%'
        context['chart_info'] = chart_info
        context['chart_obj'] = chart_obj
        context['title'] = self.get_dje_page_title(name=chart_info.name, title=chart_info.title)
        return self.template_name

    def get_dje_page_title(self, name, title, **kwargs):
        return self.page_title.format(name=name, title=title)


class DJSiteChartOptionsView(DJESiteFrontendView):
    def dje_get(self, request, *args, **kwargs) -> Any:
        chart_name = self.kwargs.get('name')
        site = kwargs.get('site')  # type: DJESite
        chart_obj, _, _ = site.resolve_chart(chart_name)
        if not chart_obj:
            return {}
        else:
            return json.loads(chart_obj.dump_options_with_quotes())


class DJESiteAboutView(DJESiteBackendView):
    template_name = ttn('about.html')


@dataclass
class SiteOpts:
    """The opts for DJESite."""
    list_layout: Literal['grid', 'list'] = 'grid'
    paginate_by: Optional[int] = None
    detail_tags_position: Literal['none', 'top', 'bottom'] = 'top'
    detail_sidebar_shown: bool = True
    nav_shown_pages: List = field(default_factory=lambda: ['home'])


class NavMenuPosition:
    SELF = 'self'
    NONE = 'none'


_SLUG_RE = re.compile(r'[-a-zA-Z0-9_]+')


class DJESite(WidgetGetterMixin):
    """A generator endpoint for visual chart site.
    Example:
        site_obj = DJESite(site_title='MySite', opts=SiteOpts(paginate_by=10))
    """

    chart_info_manager_class = LocalChartInfoManager  # type: Type[ChartInfoManagerMixin]

    def __init__(self, site_title: str, theme: str = 'bootstrap5', opts: Optional[SiteOpts] = None):
        self.site_title = site_title
        self.theme = get_theme(theme)
        if opts is None:
            self._opts = SiteOpts()
        else:
            self._opts = opts
        self.nav = Nav()
        if 'home' in self.opts.nav_shown_pages:
            self.nav.add_menu(text='首页', slug='home', url=reverse_lazy('dje_home'))
        if 'list' in self.opts.nav_shown_pages:
            self.nav.add_menu(text='All', slug='list', url=reverse_lazy('dje_list'))
        if 'collection' in self.opts.nav_shown_pages:
            self.nav.add_menu(text='Collection', slug='collection-all', url=reverse_lazy('dje_chart_collection_all'))

        self._view_dict = {
            'dje_home': DJESiteHomeView,
            'dje_list': DJESiteListView,
            'dje_chart_single': DJESiteChartSingleView,
            'dje_chart_options': DJSiteChartOptionsView,
            'dje_chart_collection': DJESiteCollectionView,
            'dje_about': DJESiteAboutView
        }
        # Inject site object to views.
        SiteInjectMixin.get_site_object = self._inject(SiteInjectMixin.get_site_object)

        # Charts & Widgets & Collections
        self._html_widgets = LazyDict()  # html_widgets
        self._chart_obj_dic = LazyDict()  # chart_widgets
        # chart_card_widgets
        self._chart_info_manager = self.chart_info_manager_class()  # type: ChartInfoManagerMixin
        self._collection_dic = {}  # type: Dict[str,WidgetCollection]

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
    def html_widgets(self) -> LazyDict:
        return self._html_widgets

    @property
    def chart_info_manager(self) -> ChartInfoManagerMixin:
        return self._chart_info_manager

    @property
    def urls(self):
        """Return the URLPattern list for site entrypoint."""
        urls = [
            path('', self._view_dict['dje_home'].as_view(), name='dje_home'),
            path('list/', self._view_dict['dje_list'].as_view(), name='dje_list'),
            path('chart/<slug:name>/', self._view_dict['dje_chart_single'].as_view(), name='dje_chart_single'),
            path('chart/<slug:name>/options/', self._view_dict['dje_chart_options'].as_view(),
                 name='dje_chart_options'),
            path('collection/', self._view_dict['dje_chart_collection'].as_view(), name='dje_chart_collection_all'),
            path('collection/<slug:name>/', self._view_dict['dje_chart_collection'].as_view(),
                 name='dje_chart_collection'),
            path('about/', self._view_dict['dje_about'].as_view(), name='dje_about')
        ]
        custom_url = self.dje_get_urls()
        if custom_url:
            urls += custom_url
        return urls

    def set_views(self, view_name: str, view_class: Type[DJESiteBackendView]):
        self._view_dict[view_name] = view_class

    # Init Widgets

    def add_left_link(self, item: LinkItem, menu_title: str = None):
        if menu_title:
            self.nav.add_item(menu_text=menu_title, item=item)
        else:
            self.nav.add_menu(text=item.text, slug=item.slug, url=item.url)
        return

    def add_right_link(self, item: LinkItem):
        """Add link on nav."""
        self.nav.add_right_link(item)
        return self

    def add_menu_item(self, item: LinkItem, menu_title: str = None):
        self.add_left_link(item, menu_title)
        return self

    def add_widgets(self, *, copyright_: Copyright = None, jumbotron: Jumbotron = None,
                    jumbotron_chart: Union[str, Any] = None, values_panel: Union[str, ValuesPanel] = None):
        """Place widgets to pages."""
        if copyright_:
            self._html_widgets.func_register(copyright_, 'copyright')
        if jumbotron:
            self._html_widgets.func_register(jumbotron, WidgetRefs.home_jumbotron)
        if isinstance(jumbotron_chart, str):
            self._chart_obj_dic.set_ref(WidgetRefs.home_jumbotron_chart, jumbotron_chart)
        elif jumbotron_chart:
            self._chart_obj_dic.func_register(jumbotron_chart, WidgetRefs.home_jumbotron_chart)
        if isinstance(values_panel, str):
            self._html_widgets.set_ref(WidgetRefs.home_values_panel, values_panel)
        elif isinstance(values_panel, ValuesPanel):
            self._html_widgets.func_register(values_panel, WidgetRefs.home_values_panel)
        return self

    # Register function and views class
    def register_chart(self, function=None, *, info: ChartInfo = None, name: str = None, title: str = None,
                       description: str = None, body: str = None, layout: str = None, top: int = 0, catalog: str = None,
                       tags: List = None, nav_parent_name: str = None, nav_after_separator: bool = False):
        """Register chart function."""

        def decorator(func):
            cname = name or func.__name__
            if not _SLUG_RE.match(cname):
                raise ValueError(f'Invalid chart slug:{cname}')
            url = reverse_lazy('dje_chart_single', args=(cname,))
            if info:
                c_info = info
            else:
                c_info = ChartInfo(name=cname, title=title or cname, description=description, body=body,
                                   url=url, top=top, catalog=catalog, tags=tags, layout=layout)
            self._chart_obj_dic.func_register(func, c_info.name)
            self._chart_info_manager.add_chart_info(c_info)
            c_nav_parent_name = nav_parent_name or catalog
            if c_nav_parent_name:
                self.nav.add_menu(text=c_nav_parent_name)
                self.nav.add_item(
                    menu_text=c_nav_parent_name,
                    item=LinkItem(text=title or cname, url=url, slug=cname),
                    after_separator=nav_after_separator
                )
            return func

        if function is None:
            return decorator
        else:
            return decorator(function)

    def resolve_chart(self, name: str) -> Tuple[Optional[Any], bool, Optional[ChartInfo]]:
        """Execute chart function and return pyecharts chart object.
        """
        if name in self._chart_obj_dic:
            func_exists = True
            chart_obj = self._chart_obj_dic.get(name)
            info_name = self._chart_obj_dic.actual_key(name)
            info = self._chart_info_manager.get_or_none(info_name)
            return chart_obj, func_exists, info
        else:
            return None, False, None

    def register_html_widget(self, function=None, *, name: str = None):
        """A short method for @DJESite.html_widgets.register"""

        def decorator(func):
            cname = name or func.__name__
            if not _SLUG_RE.match(cname):
                raise ValueError(f'Invalid widget slug:{cname}')
            self._html_widgets.func_register(func, cname)
            return func

        if function is None:
            return decorator
        else:
            return decorator(function)

    def add_collection(self, name: str, chart_names: List[str], layout: str = 'a', title: str = None,
                       catalog: str = None, nav_parent_name: str = None, nav_after_separator: bool = False):
        if not _SLUG_RE.match(name):
            raise ValueError(f'Invalid collection slug:{name}')
        collection = WidgetCollection(name=name, layout=layout)
        for chart_name in chart_names:
            collection.add_chart(chart_name)
        self._collection_dic[name] = collection
        c_nav_parent_name = nav_parent_name or catalog
        if c_nav_parent_name:
            title = title or name
            url = reverse_lazy('dje_chart_collection', args=(name,))
            self.nav.add_menu(text=c_nav_parent_name)
            self.nav.add_item(
                menu_text=c_nav_parent_name,
                item=LinkItem(text=title, url=url, slug=name),
                after_separator=nav_after_separator
            )
        return self

    def build_collection(self, name: str) -> WidgetCollection:
        if name == 'all':
            return self.build_collection_named_all()
        collection = self._collection_dic.get(name)
        collection.auto_mount(self)

    def build_collection_named_all(self) -> WidgetCollection:
        w_collection = WidgetCollection(name='all')
        for info in self.chart_info_manager.query_chart_info_list():
            chart_obj, _, _ = self.resolve_chart(info.name)
            w_collection.pack_chart_widget(chart_obj, info)
        return w_collection

    def resolve_chart_widget(self, name: str) -> Tuple[Optional[Any], bool, Optional[ChartInfo]]:
        return self.resolve_chart(name)

    def resolve_html_widget(self, name: str) -> Any:
        return self._html_widgets.get(name)

    # Public Interfaces

    def dje_get_current_theme(self, request, *args, **kwargs) -> Theme:
        """Get the theme for this request."""
        return self.theme

    def dje_get_urls(self) -> List:
        """Custom you url routes here."""
        pass
