import re
from forex_python.converter import CurrencyRates

NATION_DICT = {'eng': 'USD', 'jp': 'JPY'}

def exchange(price, lang="en"):
    c = CurrencyRates()
    exchange_rate_usd_to_krw = c.get_rate(NATION_DICT.get(lang),'KRW')
    return round(price / exchange_rate_usd_to_krw, 2)

def exchange_str_price(str_price):
    price = extract_numbers(str_price) if type(str_price) == str else str_price
    if len(price) > 0:
        return exchange(int(price))
    return price

def extract_numbers(text):
    # 정규식을 사용하여 숫자만 추출
    numbers = re.findall(r'\d+', text)
    # 추출된 숫자들을 문자열로 변환하고 모두 붙여서 반환
    return ''.join(numbers)