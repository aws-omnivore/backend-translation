from forex_python.converter import CurrencyRates

NATION_DICT = {'eng': 'USD', 'jp': 'JPY'}

def exchange(price, lang="en"):
    c = CurrencyRates()
    exchange_rate_usd_to_krw = c.get_rate(NATION_DICT.get(lang),'KRW')
    return round(price / exchange_rate_usd_to_krw, 2)

def exchange_str_price(str_price):
    return exchange(int(str_price.replace(',', '')))