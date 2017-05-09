from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import Prefetch

from rest.models import Symbol, Coin

@login_required(login_url='/login/')
def home_page(request):
    if request.method == "GET":
        coins_list = []
        symbols = Symbol.objects.all().prefetch_related('coins')

        # query evaluate here
        for symbol in symbols:
            coin = symbol.coins.all()[0]
            coins_list.append(coin)
        return render(request, 'home.html', {'coins': coins_list})

class IndexView(TemplateView):
   template_name = 'react.html'