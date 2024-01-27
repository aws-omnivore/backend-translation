from pymongo import MongoClient
import boto3
import os
from flask import Flask, request
import base64
import json
from datetime import datetime
from forex_python.converter import CurrencyRates
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# MongoDB 클라이언트 생성
mongo_client = MongoClient("localhost", 27017)

# "omnivore" 데이터베이스 선택
db = mongo_client["omnivore"]

# "store" 컬렉션 선택
collection = db["store"]

aws_access_key_id = os.environ.get('aws_access_key_id')
aws_secret_access_key = os.environ.get('aws_secret_access_key')

# Amazon Translate 클라이언트 생성
translate_client = boto3.client('translate', region_name='ap-northeast-2', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)

def get_store_info(store_name):
    # MongoDB에서 가게 이름에 해당하는 데이터 조회
    store_info = collection.find_one({"name": store_name})
    return store_info

nation_dic = {'eng': 'USD', 'jp': 'JPY'}
# 환율 계산
def ex_list(price_list, Lang='en'):
    for i in range(len(price_list)):
        c = CurrencyRates()
        Price=price_list[i]
        exchange_rate_usd_to_krw = c.get_rate(nation_dic.get(Lang),'KRW')
        ex_result = round(Price / exchange_rate_usd_to_krw, 2)
        price_list[i]=ex_result
    return price_list

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


def log_function_execution_time(func):  # func : api_test, 데코레이터로 log_function_execution_time 함수를 실행하였으므로 매개변수로 api_test를 가져온다.
    def wrapper():
        headers = request.headers
        body = request.get_json() # body 꺼내오는 함수
        # jwt decode
        decoded_dict = token_decode(headers)

        result = func(body) # api_test 함수 실행

        #현재 년월일시분초를 가져와서 로그에 추가
        current_time = datetime.now()
        
        db=mongo_client['log']
        collection = db['time']

        #로그를 mongoDB에 저장
        log_entry = {
            "timestamp": current_time,
            "store_name": body["name"], # request body
            "translate_name": result[0]["name"], # response
            "email" : decoded_dict['email'] # auth email
        }
        collection.insert_one(log_entry)
     
        return result
    
    return wrapper


def token_decode(headers):
    value = headers.get("Authorization")
    v = value.split(" ")[1]

    # JWT payload 추출
    payload_encoded = v.split('.')[1]

    # Base64 디코딩
    payload_bytes = base64.urlsafe_b64decode(payload_encoded + '==')
    decoded_payload = payload_bytes.decode('utf-8')
    payload_dict = json.loads(decoded_payload)

    return payload_dict

def translate_store_info(store_info, target_language='en'): # target_language는 유저정보 받아오는 data에 따라 바뀔 것
    if store_info:
        # 가게 정보에서 번역 대상 텍스트 추출 (이 예제에서는 'name' 필드를 번역합니다)
        name_to_translate = store_info.get('name', '')
        menu_to_translate = store_info.get('menu', '')
        price_to_translate = store_info.get('price', '')


        # Amazon Translate를 사용하여 텍스트 번역
        translate_response_name = translate_client.translate_text(
            Text= name_to_translate, 
            SourceLanguageCode='ko',  # 가게 이름이 한국어로 되어 있다고 가정
            TargetLanguageCode=target_language
        )
        translated_text_name = translate_response_name['TranslatedText']
        # 메뉴 번역
        translated_text_menu = []
        # 1. 리스트이면
        if type(menu_to_translate) == list:
            # 2. 하나씩 꺼내서 
            for a in menu_to_translate:
                # 3. 번역하도록 요청한다.
                translate_response_menu = translate_client.translate_text(
                    Text= a, 
                    SourceLanguageCode='ko',  # 메뉴가 한국어로 되어 있다고 가정
                    TargetLanguageCode=target_language
                )
                # 4. append를 써줘서 리스트에 추가한다.
                translated_text_menu.append(translate_response_menu['TranslatedText'])

        # 1. 딕셔너리면
        translated_text_price = {}
        if type(price_to_translate) == dict:
            # 2. dictionary에서 items 함수를 써줘서 하나씩 꺼낸다.
            for key, value in price_to_translate.items():
                # 3. 번역하도록 요청한다.
                translate_response_price = translate_client.translate_text(
                    Text= key, 
                    SourceLanguageCode='ko',  # 가격이 한국어로 되어 있다고 가정
                    TargetLanguageCode=target_language
                )
                # 4. dictionary[key]=value 형식으로 딕셔너리에 추가한다.
                translated_text_price[translate_response_price['TranslatedText']]=value

        translated_store = {}
        translated_store["name"]=translated_text_name
        translated_store["menu"]=translated_text_menu
        translated_store["price"]= translated_text_price

        return translated_store
    else:
        return None

@app.route('/test', methods=['POST'])
@log_function_execution_time
def api_test(body):
    translated_name = translate_store_info(body, target_language='en')
    price_list = list(translated_name.get("price",{}).values())
    updated_data = replace_price_values(translated_name, ex_list(price_list))
    return updated_data, 200

app.run(host="localhost",port=5001)