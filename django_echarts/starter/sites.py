import re
import sys
from collections import defaultdict
from functools import wraps
from typing import Optional, List, Dict, Type, Any, Union

from borax.serialize import cjson
from borax.system import load_object
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.urls import reverse_lazy, path
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.views.generic.edit import FormMixin
from django_echarts.ajax_echarts import ChartOptionsView
from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
from django_echarts.core.exceptions import DJEAbortException, ChartDoesNotExist
from django_echarts.entities import (
    ChartInfo, WidgetCollection, Nav, Menu, LinkItem, Jumbotron, Copyright, Message, ValuesPanel, LinkGroup
)
from django_echarts.entities.uri import EntityURI, ParamsConfig
from django_echarts.custom_maps import custom_map_urlpatterns
from django_echarts.site_exts import reverse_chart_url
from django_echarts.stores.entity_factory import factory
from django_echarts.utils.compat import compat_get_elided_page_range
from typing_extensions import Literal

from .optstools import SiteOptsForm, SiteOpts

__all__ = ['DJESite', 'DJESiteBackendView', 'DJESiteFrontendView']

_VAR_CHART_ = 'chart_obj'
_VAR_CHART_INFO_ = 'chart_info'
_VAR_PAGE_CONTAINER_ = 'widget_collection'


class WidgetRefs:
    """Used for context variable names."""
    home_jumbotron = 'home_jumbotron'
    home_jumbotron_chart = 'home_jumbotron_chart'
    home_values_panel = 'home_values_panel'


class SiteInjectMixin:
    @staticmethod
    def get_site_object(site: 'DJESite' = None):
        return site


class DJESiteBackendView(TemplateResponseMixin, ContextMixin, SiteInjectMixin, View):
    """The base view for Site.
    """

    def get(self, request, *args, **kwargs):
        site = SiteInjectMixin.get_site_object()
        context = self.get_context_data(site=site, **kwargs)  # TODO ? DJEAbortException in get_context_data
        try:
            template_name = self.dje_init_page_context(context=context, site=site)
            if isinstance(template_name, dict):
                raise TypeError(
                    'The method dje_init_page_context should return a string for template name.Not a dict for context.')
        except DJEAbortException as e:
            context['message'] = Message(e.message, catalog='warning')
            template_name = 'message.html'
        return self._render_to_response(context, template_name=template_name)

    def _render_to_response(self, context, template_name=None, **kwargs):
        template_name = template_name or self.template_name
        return self.response_class(
            request=self.request,
            template=template_name,
            context=context,
            using=self.template_engine
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = kwargs.get('site')  # type: DJESite
        if site is None:
            # the get_context_data is called by other ContextMixin class in django.
            site = SiteInjectMixin.get_site_object()
        context['nav'] = site.nav
        context['site_title'] = site.site_title
        context['page_title'] = site.site_title
        context['copyright'] = factory.get_widget_by_uri(site.ref2uri['copyright'])
        context['opts'] = site.opts

        # The data store in a view processing lifecycle.
        self.extra_context = {}
        return context

    # Interfaces

    def abort_request(self, message: str):
        """Abort current request and show the message page."""
        raise DJEAbortException(message)

    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        """Update context and return its template name.
        If no template name returned, use the value returned by self.dje_get_template_name
        """
        pass


class DJESiteDetailBaseView(DJESiteBackendView):
    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        chart_name = self.kwargs.get('name')
        chart_info = factory.chart_info_manager.get_or_none(chart_name)
        context['chart_info'] = chart_info
        if not chart_info:
            self.abort_request('The chart does not exist.')
        return self.template_name


class DJESiteCollectionView(DJESiteBackendView):
    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        collection_name = self.kwargs.get('name', 'all')
        widget_collection = site.build_collection(collection_name)
        if not widget_collection:
            self.abort_request(f'The collection {collection_name} contains no data..')
        context[_VAR_PAGE_CONTAINER_] = widget_collection
        return 'chart_collection.html'


class DJESiteFrontendView(SiteInjectMixin, View):
    """The helper view class for ajax request."""

    def get(self, request, *args, **kwargs):
        site = SiteInjectMixin.get_site_object()
        data = self.dje_get(request, site=site, *args, **kwargs)
        if isinstance(data, JsonResponse):
            return data
        else:
            return JsonResponse(data, safe=False, encoder=cjson.CJSONEncoder)

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
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        site = SiteInjectMixin.get_site_object()
        context = super(DJESiteHomeView, self).get_context_data(**kwargs)
        context['jumbotron'] = factory.get_widget_by_uri(site.ref2uri[WidgetRefs.home_jumbotron])
        chart_obj, _, info = factory.get_chart_and_info_by_uri(site.ref2uri[WidgetRefs.home_jumbotron_chart])
        if chart_obj:
            context[_VAR_CHART_] = chart_obj
            context[_VAR_CHART_INFO_] = info
        context[WidgetRefs.home_values_panel] = factory.get_widget_by_uri(
            site.ref2uri[WidgetRefs.home_values_panel])
        context['top_chart_info_list'] = factory.chart_info_manager.query_chart_info_list(with_top=True)
        context['layout_tpl'] = 'items_grid.html'
        return context


class DJESiteListView(DJESiteBackendView):
    template_name = 'list.html'
    paginate_by = None
    list_layout = 'list'
    page_kwarg = 'page'
    query_kwarg = 'query'

    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        layout_str = self.request.GET.get('layout', site.opts.list_layout)
        if layout_str not in ('grid', 'list'):
            layout_str = 'grid'
        context['layout_tpl'] = f'items_{layout_str}.html'
        query_string = self.request.GET.get(self.query_kwarg)
        qs = {}
        if query_string:
            qs.update({'keyword': query_string})
            context['keyword'] = query_string
        chart_info_list = factory.chart_info_manager.query_chart_info_list(**qs)
        paginate_by = site.opts.paginate_by
        if paginate_by:
            paginator = Paginator(chart_info_list, paginate_by, allow_empty_first_page=True)
            page_number = self.request.GET.get(self.page_kwarg, 1)
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
            elided_page_nums = compat_get_elided_page_range(paginator, page_number)
            context['elided_page_nums'] = list(elided_page_nums)
            return 'list_with_paginator.html'
        else:
            context['chart_info_list'] = chart_info_list
            return 'list.html'


class DJESiteChartSingleView(DJESiteBackendView):
    template_name = 'chart_single.html'

    charts_config = []
    page_title = '{title}'

    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        context['view_name'] = 'dje_chart_single'
        chart_name = self.kwargs.get('name')
        chart_uri = EntityURI.from_params_path('chart', chart_name, self.kwargs.get('chart_params', ''))
        is_parametric = factory.clean_uri_params(chart_uri)
        if len(chart_uri.params) == 0 and is_parametric:
            return self.update_context_for_parametric_chart_without_params(context, chart_uri)
        # TODO exception ChartDoesNotExist ChartParamsInvalid
        try:
            chart_obj, func_exists, chart_info = factory.get_chart_and_info_by_uri(chart_uri)
            if not func_exists:
                self.abort_request('The chart does not exist.')
            if not chart_obj:
                self.abort_request(f'The chart function {chart_name} returns nothing..')
            chart_obj.width = '100%'
            context['chart_info'] = chart_info
            context['chart_obj'] = chart_obj
            context['title'] = self.get_dje_page_title(name=chart_info.name, title=chart_info.title)
            return self.template_name
        except ChartDoesNotExist as e:
            self.abort_request(str(e))

    def update_context_for_parametric_chart_without_params(self, context, uri: EntityURI):
        chart_info = factory.chart_info_manager.get_or_none(uri=uri)
        context['chart_info'] = chart_info
        context['title'] = self.get_dje_page_title(name=chart_info.name, title=chart_info.title)
        link_group = LinkGroup()
        for params_dic in chart_info.params_config:
            link = LinkItem(
                text=chart_info.title.format(**params_dic),
                url=reverse_chart_url(EntityURI('chart', chart_info.name, params_dic))
            )
            link_group.add_widget(link)
        context['link_group'] = link_group
        return 'chart_parametric.html'

    def get_dje_page_title(self, name, title, **kwargs):
        return self.page_title.format(name=name, title=title)


class DJESiteAboutView(DJESiteBackendView):
    template_name = 'about.html'


class DJESiteSettingsView(FormMixin, DJESiteBackendView):
    form_class = SiteOptsForm
    template_name = 'settings.html'
    success_url = reverse_lazy('dje_settings')  # self page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_obj = self.get_form()
        context['form'] = form_obj
        return context

    def get_initial(self):
        opts = SiteInjectMixin.get_site_object().opts
        return {
            'nav_top_fixed': opts.nav_top_fixed,
            'list_layout': opts.list_layout,
            'paginate_by': opts.paginate_by or 0,
            'theme_palette_name': DJANGO_ECHARTS_SETTINGS.theme.theme_palette
        }

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        opts = SiteInjectMixin.get_site_object().opts
        opts.nav_top_fixed = form.cleaned_data['nav_top_fixed']
        opts.list_layout = form.cleaned_data['list_layout']
        opts.paginate_by = form.cleaned_data['paginate_by']
        DJANGO_ECHARTS_SETTINGS.switch_palette(form.cleaned_data['theme_palette_name'])
        return super().form_valid(form)


class NavMenuPosition:
    SELF = 'self'
    NONE = 'none'


_SLUG_RE = re.compile(r'[-a-zA-Z0-9_]+')


class NavBuilder:
    @staticmethod
    def build_nav(left_menu_config: list = None, right_menu_config: list = None,
                  footer_links_config: list = None):
        left_menu_config = left_menu_config or []
        right_menu_config = right_menu_config or []
        footer_links_config = footer_links_config or []
        nav = Nav()
        NavBuilder._build_nav(left_menu_config, nav.left_menus)
        NavBuilder._build_nav(right_menu_config, nav.right_menus)
        for data in footer_links_config:
            link = LinkItem(**NavBuilder._parse_params(data))
            nav.footer_links.append(link)
        return nav

    @staticmethod
    def build_default_nav(nav_shown_pages: list):
        return NavBuilder.build_nav(left_menu_config=nav_shown_pages)

    @staticmethod
    def _build_nav(menu_config: list, menu_container: list):
        for data in menu_config:
            menu = None
            if isinstance(data, str):
                menu = Menu(**NavBuilder._parse_params(data))
            elif isinstance(data, dict):
                if 'view_name' in data or 'url' in data:
                    menu = Menu(**NavBuilder._parse_params(data))
                elif 'children' in data:
                    menu = Menu(**NavBuilder._parse_params(data))
                    for data_item in data['children']:
                        link_item = LinkItem(**NavBuilder._parse_params(data_item))
                        menu.children.append(link_item)
            menu_container.append(menu)

    @staticmethod
    def _parse_params(val: Union[str, dict]):
        # todo handle uri
        if isinstance(val, str):
            if val == Nav.CHART_PLACEHOLDER:
                return dict(text=val)
            elif val == 'home':
                return dict(text='首页', slug='home', url=reverse_lazy('dje_home'))
            elif val == 'list':
                return dict(text='所有', slug='list', url=reverse_lazy('dje_list'))
            elif val == 'collection':
                return dict(text='合辑', slug='collection-all', url=reverse_lazy('dje_chart_collection_all'))
            elif val == 'settings':
                return dict(text='设置', slug='settings', url=reverse_lazy('dje_settings'))
            else:
                return dict(text=val)
        elif isinstance(val, dict):
            if 'view_name' in val:
                return dict(text=val.get('text'), slug=val.get('slug'),
                            url=reverse_lazy(val['view_name'], kwargs=val.get('kwargs', {})))
            elif 'url' in val:
                if val['url'].startswith('chart:'):
                    uri = EntityURI.from_str(val['url'])
                    url = reverse_lazy('dje_chart_single', args=[uri.name, uri.params_path])
                else:
                    url = val['url']
                return dict(text=val.get('text'), slug=val.get('slug'), url=url)
            elif 'children' in val:
                return dict(text=val.get('text'), slug=val.get('slug'))


class DJESite:
    """A generator endpoint for visual chart site.
    Example:
        site_obj = DJESite(site_title='MySite', opts=SiteOpts(paginate_by=10))
    """

    def __init__(self, site_title: str, opts: Optional[SiteOpts] = None, ignore_register_nav: bool = False):
        self.site_title = site_title
        self.ignore_register_nav = ignore_register_nav
        self._custom_urlpatterns = []  # url entry
        if opts is None:
            self._opts = SiteOpts()
        else:
            self._opts = opts
        self.nav = NavBuilder.build_default_nav(self._opts.nav_shown_pages)
        self._chart_nav = Nav()
        self._view_dict = {
            'dje_home': DJESiteHomeView,
            'dje_list': DJESiteListView,
            'dje_chart_single': DJESiteChartSingleView,
            'dje_chart_options': ChartOptionsView,
            'dje_chart_collection': DJESiteCollectionView,
            'dje_about': DJESiteAboutView,
            'dje_settings': DJESiteSettingsView
        }
        # Inject site object to views.
        SiteInjectMixin.get_site_object = self._inject(SiteInjectMixin.get_site_object)

        self._collection_dic = {}  # type: Dict[str,WidgetCollection]

        self._ref2uri = defaultdict(EntityURI.empty)

    def _inject(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            selected_deps = {'site': self}
            new_kwargs = {**kwargs, **selected_deps}
            return func(*args, **new_kwargs)

        return decorated

    @property
    def ref2uri(self):
        return self._ref2uri

    @property
    def opts(self) -> SiteOpts:
        return self._opts

    @property
    def urls(self):
        """Return the URLPattern list for site entrypoint."""
        urls = [
            path('', self._view_dict['dje_home'].as_view(), name='dje_home'),
            path('list/', self._view_dict['dje_list'].as_view(), name='dje_list'),
            path('chart/<slug:name>/', self._view_dict['dje_chart_single'].as_view(), name='dje_chart_single'),
            path('chart/<slug:name>/options/', self._view_dict['dje_chart_options'].as_view(),
                 name='dje_chart_options'),
            path('chart/<slug:name>/<path:chart_params>/', self._view_dict['dje_chart_single'].as_view(),
                 name='dje_chart_single'),
            path('collection/', self._view_dict['dje_chart_collection'].as_view(), name='dje_chart_collection_all'),
            path('collection/<slug:name>/', self._view_dict['dje_chart_collection'].as_view(),
                 name='dje_chart_collection'),
            path('about/', self._view_dict['dje_about'].as_view(), name='dje_about'),
            path('settings/', self._view_dict['dje_settings'].as_view(), name='dje_settings'),

        ]
        urls += custom_map_urlpatterns + self._custom_urlpatterns
        return urls

    def extend_urlpatterns(self, urlpatterns):
        self._custom_urlpatterns.extend(urlpatterns)

    def register_view(
            self,
            view_name: Literal[
                'dje_home', 'dje_list', 'dje_chart_single', 'dje_chart_collection', 'dje_about', 'dje_settings'],
            view_class: Type[DJESiteBackendView]
    ):
        self._view_dict[view_name] = view_class

    def config_nav(self, nav_config: dict = None):
        """fill nav from a config dict."""
        if nav_config:
            self.nav = NavBuilder.build_nav(
                left_menu_config=nav_config.get('nav_left'),
                right_menu_config=nav_config.get('nav_right'),
                footer_links_config=nav_config.get('nav_footer'),
            )
        holder_index = -1
        for i, menu in enumerate(self.nav.left_menus):
            if menu.text == Nav.CHART_PLACEHOLDER:
                holder_index = i
                break
        if holder_index == -1:
            return self
        self.nav.left_menus = self.nav.left_menus[:holder_index] + self._chart_nav.left_menus + self.nav.left_menus[
                                                                                                holder_index + 1:]
        return self

    def load_config_from_module(self, module_path: str):
        """Load config from a python module."""
        __import__(module_path)
        mod = sys.modules[module_path]
        nav_config = getattr(mod, 'nav_config')
        self.config_nav(nav_config)

    # Init Widgets

    def add_widgets(self, *, copyright_: Copyright = None, jumbotron: Jumbotron = None,
                    jumbotron_chart: Union[str, Any] = None, values_panel: Union[str, ValuesPanel] = None):
        """Place widgets to pages."""

        self._add_widget('copyright', copyright_, 'widget')
        self._add_widget(WidgetRefs.home_jumbotron, jumbotron, 'widget')
        self._add_widget(WidgetRefs.home_jumbotron_chart, jumbotron_chart, 'chart')
        self._add_widget(WidgetRefs.home_values_panel, values_panel, 'widget')
        return self

    def _add_widget(self, ref_name: str, entity_obj_or_name=None, entity_catalog: str = None):
        if entity_obj_or_name is None:
            return
        if isinstance(entity_obj_or_name, str):
            uri = EntityURI.from_str(entity_obj_or_name, catalog=entity_catalog)
        else:
            uri = EntityURI.from_str(ref_name, catalog=entity_catalog)
            if entity_catalog == 'chart':
                factory.register_chart_widget(entity_obj_or_name, uri.name)
            else:
                factory.register_html_widget(entity_obj_or_name, uri.name)
        self._ref2uri[ref_name] = uri

    # Register function and views class
    def register_chart(self, function=None, *, info: ChartInfo = None, name: str = None, title: str = None,
                       description: str = None, body: str = None, layout: str = None, top: int = 0, catalog: str = None,
                       tags: List = None, nav_parent_name: str = None, nav_after_separator: bool = False,
                       params_config: ParamsConfig = None):
        """Register chart function."""

        def decorator(func):
            cname = name or func.__name__
            if not _SLUG_RE.match(cname):
                raise ValueError(f'Invalid chart slug:{cname}')
            url = reverse_lazy('dje_chart_single', args=(cname,))  # TODO
            if info:
                c_info = info
            else:
                c_info = ChartInfo(name=cname, title=title or cname, description=description, body=body, url=url,
                                   top=top, catalog=catalog, tags=tags, layout=layout, params_config=params_config)
            factory.register_chart_widget(func, c_info.name, info=c_info)
            # TODO Delete menu register for single chart
            #
            if nav_parent_name == 'self':
                self._chart_nav.add_left_menu(text=title or cname, slug=cname, url=url)
            elif nav_parent_name == 'none':
                pass
            else:
                c_nav_parent_name = nav_parent_name or catalog
                if c_nav_parent_name:
                    self._chart_nav.add_left_menu(text=c_nav_parent_name)
                    self._chart_nav.add_item_in_left_menu(
                        menu_text=c_nav_parent_name,
                        item=LinkItem(text=title or cname, url=url, slug=cname),
                        after_separator=nav_after_separator
                    )
            return func

        if function is None:
            return decorator
        else:
            return decorator(function)

    def register_html_widget(self, function=None, *, name: str = None):
        """Define a html widget."""

        def decorator(func):
            cname = name or func.__name__
            if not _SLUG_RE.match(cname):
                raise ValueError(f'Invalid widget slug:{cname}')
            factory.register_html_widget(func, cname)
            return func

        if function is None:
            return decorator
        else:
            return decorator(function)

    def register_collection(self, function=None, name: str = None, title: str = None,
                            catalog: str = None, nav_parent_name: str = None, nav_after_separator: bool = False):
        def decorator(func):
            cname = name or func.__name__
            if isinstance(func, WidgetCollection):
                self._collection_dic[cname] = func
            elif callable(func):
                collection = func()
                self._collection_dic[cname] = collection
            else:
                pass
            url = reverse_lazy('dje_chart_collection', args=(cname,))
            c_title = title or name
            if nav_parent_name == 'self':
                self._chart_nav.add_left_menu(text=c_title, url=url)
            elif nav_parent_name == 'none':
                pass
            else:
                c_nav_parent_name = nav_parent_name or catalog
                self._chart_nav.add_left_menu(text=c_nav_parent_name)
                self._chart_nav.add_item_in_left_menu(
                    menu_text=c_nav_parent_name,
                    item=LinkItem(text=c_title, url=url, slug=name),
                    after_separator=nav_after_separator
                )
            return func

        if function is None:
            return decorator
        else:
            return decorator(function)

    def build_collection(self, name: str) -> WidgetCollection:
        if name == 'all':
            return self._build_collection_named_all()
        collection = self._collection_dic.get(name)
        collection.auto_mount(factory)
        return collection

    def _build_collection_named_all(self) -> WidgetCollection:
        w_collection = WidgetCollection(name='all', layout='s8')
        for info in factory.chart_info_manager.query_chart_info_list():
            chart_obj = factory.get_chart_widget(info.name)
            w_collection.pack_chart_widget(chart_obj, info)
        return w_collection

    @classmethod
    def load_from_yaml(cls, yaml_file: str):
        return cls(ignore_register_nav=True)
