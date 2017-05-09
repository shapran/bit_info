import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest.settings')


# from django.conf import settings
import django

django.setup()
from rest.models import Symbol, Coin
from spider import start

r = start()

for item in r:
    symbol_name = item['name']
    symbol_symb = item['symbol']

    try:
        Symbol_item = Symbol.objects.get_or_create(name=symbol_name, symbol=symbol_symb)

        Coin_item = Coin(symbol=Symbol_item[0], market_cap=item['market_cap'], price=item['price'], supply=item['circ_supply'],
                         volume=item['volume'], hour_prc=item['hour_volume'], day_prc=item['day_volume'],
                         week_prc=item['week_volume'])

        Coin_item.save()
    except Exception as err:
        print(item['name'], item['price'], item['circ_supply'], item['volume'])
        print(err)
