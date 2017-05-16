import asyncio
import aiohttp
from lxml import html
import re
pattern_price = re.compile(r'([\d.,]+)')
pattern_percent = re.compile(r'([\d.,-]+)')

async def createSessin():
    HEADERS = {
        ':authority': 'coinmarketcap.com',
        ':method': 'GET',
        ':path': '/ all / views / all /',
        ':scheme': 'https',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, lzma, sdch',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'pragma': 'no-cache',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36 OPR/41.0.2353.69',
    }
    session = aiohttp.ClientSession(headers=HEADERS)
    return session

def fieldFilter(field):
    field = field.strip()

    if '?' in field:
        field = 0.0
    elif '%' not in field:
        amount = re.findall(pattern_price, field)
        if amount:
            if ',' in amount[0]:
                field = float(amount[0].replace(',', ''))
            else:
                field = float(amount[0])
        else:
            field = 0.0
    elif '%' in field:
        amount = re.findall(pattern_percent, field)
        if amount:
            field = float(amount[0])
        else:
            field = 0.0
    return field

def serialize(fields):
    name, symbol, market_cap, price, circ_supply, volume, hour_volume, day_volume, week_volume = fields

    #filters
    market_cap = fieldFilter(market_cap)
    price = fieldFilter(price)
    circ_supply = fieldFilter(circ_supply)
    volume = fieldFilter(volume)
    hour_volume = fieldFilter(hour_volume)
    day_volume = fieldFilter(day_volume)
    week_volume = fieldFilter(week_volume)

    data = {
        'name': str(name),
        'symbol': str(symbol),
        'market_cap': market_cap,
        'price': price,
        'circ_supply': circ_supply,
        'volume': volume,
        'hour_volume': hour_volume,
        'day_volume': day_volume,
        'week_volume': week_volume
    }

    return data

def parse(content):
    serialized_data = []
    root = html.fromstring(content)

    coin_types = root.xpath('//table[@id="currencies-all"]/tbody/tr')

    for item in coin_types:
        name = item.xpath('./td[@class="no-wrap currency-name"]/a/text()')[0]
        symbol = item.xpath('./td[@class="text-left"]/text()')[0]
        market_cap = item.xpath('./td[@class="no-wrap market-cap text-right"]/text()')[0]

        value_indicators = item.xpath('./td[(@class="no-wrap text-right") or (@class="no-wrap text-right ")]')

        price = ''.join(value_indicators[0].xpath('./descendant-or-self::text()'))
        circ_supply = ''.join(value_indicators[1].xpath('./descendant-or-self::text()'))
        volume = ''.join(value_indicators[2].xpath('./descendant-or-self::text()'))

        hour_volume = ''.join(item.xpath('./td[starts-with(@class,"no-wrap percent-1h")]/text()'))
        day_volume = ''.join(item.xpath('./td[starts-with(@class,"no-wrap percent-24h")]/text()'))
        week_volume = ''.join(item.xpath('./td[starts-with(@class,"no-wrap percent-7d")]/text()'))

        field = serialize((name, symbol, market_cap, price, circ_supply, volume, hour_volume, day_volume, week_volume))
        serialized_data.append(field)

    return serialized_data



async def main():
    URL = 'https://coinmarketcap.com/all/views/all/'
    result = None

    session = await createSessin()

    async with session.get(URL) as response:
        if response.status == 200:
            content = await response.text()
            result = parse(content)
        else:
            print('Response != 200')

    session.close()
    return result

def start():
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    result = event_loop.run_until_complete(main())
    return result
