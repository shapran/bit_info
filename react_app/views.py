from django.shortcuts import render
from django.views.generic.base import TemplateView, TemplateResponse

class IndexPageView(TemplateView):
    def get_context_data(self, request=None, **kwargs):
        context = {}
        return context

    def get(self, request):
        context = self.get_context_data(request)

        return TemplateResponse(request, template="react_test.html", context=context)