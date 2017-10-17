from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from .utils import get_merged, get_tobuy


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['data'] = get_merged()
        return context


class RequiredStuffView(View):
    def get(self, request, *args, **kwargs):
        data = get_tobuy()
        return JsonResponse(data, status=200)
