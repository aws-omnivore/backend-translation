from forex_python.converter import CurrencyRates

NATION_DICT = {'eng': 'USD', 'jp': 'JPY'}

# 환율 계산
def ex_list(price_list, Lang='en'):
    for i in range(len(price_list)):
        c = CurrencyRates()
        Price=price_list[i]
        exchange_rate_usd_to_krw = c.get_rate(NATION_DICT.get(Lang),'KRW')
        ex_result = round(Price / exchange_rate_usd_to_krw, 2)
        price_list[i]=ex_result
    return price_list

def exchange(price, lang="en"):
    c = CurrencyRates()
    exchange_rate_usd_to_krw = c.get_rate(NATION_DICT.get(lang),'KRW')
    return round(price / exchange_rate_usd_to_krw, 2)

def exchange_str_price(str_price):
    return exchange(int(str_price.replace(',', '')))

#환전된 price 리스트 -> 딕셔너리 value 치환
def replace_price_values(input_dict, new_values):
    # "price" 필드가 없을 경우 입력 딕셔너리를 그대로 반환
    if "price" not in input_dict:
        return input_dict
    
    # "price" 필드의 값들을 차례대로 새로운 값들로 치환
    replaced_prices = {menu: new_value for menu, new_value in zip(input_dict["price"], new_values)}

    # 입력 딕셔너리를 복사하여 변경된 "price" 필드로 업데이트
    updated_dict = input_dict.copy()
    updated_dict["price"] = replaced_prices

    return updated_dict