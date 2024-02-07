from pymongo import MongoClient
import boto3
import os
from dotenv import load_dotenv
load_dotenv()

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

def translate_data(data_to_translate, target_language):
    for a in data_to_translate:
        # 3. 번역하도록 요청한다.
        translated_response_data = translate_client.translate_text(
            Text= a, 
            SourceLanguageCode='ko',  # 메뉴가 한국어로 되어 있다고 가정
            TargetLanguageCode=target_language
        )
    return translated_response_data


def translate_store_info(store_info, target_language='en'):
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

# 가게 이름
store_name = "한솥"

# 가게 정보 가져오기
store_info = get_store_info(store_name)

if store_info:
    # 번역된 가게 이름 출력
    translated_name = translate_store_info(store_info)
    print(f"{translated_name}")
else:
    print(f"{store_name}에 해당하는 가게 정보가 없습니다.")