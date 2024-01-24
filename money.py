from pymongo import MongoClient
from forex_python.converter import CurrencyRates
#from currency_converter import CurrencyConverter
client=MongoClient(host='localhost',port=27017)

db=client['omnivore']
collection = db['store']
ins={'name':'kimbab','price':3000}
nation_dic = {'eng': 'USD', 'jp': 'JPY'}
#Lang='eng' #언어 불러올 때 인자로 넣어버리기
#collection.insert_one(ins)

result = collection.find({}, {'_id': 0, 'price': 1})
for document in result:
    Price=(document['price'])


def exchange(Lang=''):
    c = CurrencyRates()
    # 실시간 환율 받아오기
    exchange_rate_usd_to_krw = c.get_rate(nation_dic.get(Lang),'KRW')
    # 변환
    #amount_krw = Price
    ex_result = round(Price / exchange_rate_usd_to_krw, 2)
    #ex_result = Price / exchange_rate_usd_to_krw
    return ex_result


e_result= exchange('jp') #여기 이 부분 나중에 언어 선택하는 그거로 바꿔오기
print(e_result)



'''
c = CurrencyConverter()
#convert(금액, 기준통화, 변환될통화)
print(int(c.convert(Price,'KRW',nation_dic.get(Lang))))
'''