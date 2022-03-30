from typing import Any

from django.views.generic.base import TemplateView


class PageTemplateView(TemplateView):
    template_name = 'simple/page.html'

    def get_context_data(self, **kwargs):
        context = super(PageTemplateView, self).get_context_data(**kwargs)
        context['container_obj'] = self.get_container_obj()
        return context

    def get_container_obj(self) -> Any:
        pass
