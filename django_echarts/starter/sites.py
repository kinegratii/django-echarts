from functools import wraps
from typing import Type

from django.urls import reverse_lazy, path
from django.views.generic.base import TemplateView

from .html_widgets import Nav, LinkItem

__all__ = ['DJESite', 'DJESiteHomeView', 'DJESiteDetailView', 'DJESiteListView']


class DJESiteBaseView(TemplateView):
    dje_theme = 'bootstrap3'

    def get_template_names(self):
        return [self.template_name.format(theme=self.dje_theme)]

    @staticmethod
    def get_site_object(site: 'DJESite' = None):
        return site

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = DJESiteBaseView.get_site_object()
        context['nav'] = site.nav
        context['site_title'] = site.site_title
        return context

    def get_dje_nav(self):
        pass


class DJESiteHomeView(DJESiteBaseView):
    template_name = '{theme}/home.html'


class DJESiteListView(DJESiteBaseView):
    template_name = '{theme}/list.html'


class DJESiteDetailView(DJESiteBaseView):
    template_name = '{theme}/detail.html'

    charts_config = []
    page_title = '{description}'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'dje_detail'
        context['title'] = 'My Charts'
        chart_name = self.kwargs.get('name')
        context['menu'] = []
        found = False
        for values in self.charts_config:
            name, description, *_ = values
            if chart_name == name and not found:
                found = True
                func = getattr(self, f'dje_chart_{name}', None)
                if func:
                    chart_obj = func()
                    context['chart_obj'] = chart_obj
                context['title'] = self.get_dje_page_title(name=name, description=description)
                context['menu'].append((name, description, True))
            else:
                context['menu'].append((name, description, False))
        if found:
            tpl = '{theme}/detail.html'.format(theme=self.dje_theme)
        else:
            tpl = '{theme}/empty.html'.format(theme=self.dje_theme)
        return self.response_class(
            request=self.request,
            template=tpl,
            context=context,
            using=self.template_engine
        )

    def get_dje_page_title(self, name, description, **kwargs):
        return self.page_title.format(name=name, description=description)


class DJESite:
    def __init__(self, site_title: str = 'My Charts Demo', theme: str = 'bootstrap3', url_prefix: str = ''):
        self.site_title = site_title
        self.theme = theme
        self.url_prefix = url_prefix
        self.nav = Nav().add_menu(title='首页', slug='home', url=reverse_lazy('dje_home'))
        self._view_dict = {
            'home': DJESiteHomeView,
            'detail': DJESiteDetailView,
            'list': DJESiteListView
        }

        DJESiteBaseView.get_site_object = self._inject(DJESiteBaseView.get_site_object)

    def _inject(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            selected_deps = {'site': self}
            new_kwargs = {**kwargs, **selected_deps}
            return func(*args, **new_kwargs)

        return decorated

    def add_link(self, item: LinkItem):
        self.nav.add_right_link(item)
        return self

    def register_home_view(self, view_class: Type[DJESiteHomeView], ):
        self._view_dict['home'] = view_class

    def register_list_view(self, view_class: Type[DJESiteListView]):
        pass

    def register_detail_view(self, view_class: Type[DJESiteDetailView], name: str):
        self._view_dict['detail'] = view_class
        self.nav.add_menu(title=name)
        for _name, _description in view_class.charts_config:
            self.nav.add_item(
                menu_title=name,
                item=LinkItem(title=_description, url=reverse_lazy('dje_detail', args=(_name,)), slug=_name)
            )

    def as_urls(self):
        return [
            path('', self._view_dict['home'].as_view(), name='dje_home'),
            path('list/', self._view_dict['list'].as_view(), name='dje_list'),
            path('detail/<slug:name>/', self._view_dict['detail'].as_view(), name='dje_detail')
        ]


class DJEModelSite:
    def discover(self):
        pass
