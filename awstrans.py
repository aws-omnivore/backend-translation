from flask import Flask
from dotenv import load_dotenv
load_dotenv()

from utils.logger import log_function_execution_time
from utils.db import get_store_info
from utils.exchange_money import ex_list, replace_price_values
from utils.aws_trans import translate_text

app = Flask(__name__)

def translate_store_info(store_info, target_language='en'): # target_language는 유저정보 받아오는 data에 따라 바뀔 것
    if store_info:
        # 가게 정보에서 번역 대상 텍스트 추출 (이 예제에서는 'name' 필드를 번역합니다)
        name_to_translate = store_info.get('name', '')
        menu_to_translate = store_info.get('menu', '')
        price_to_translate = store_info.get('price', '')


        # Amazon Translate를 사용하여 텍스트 번역
        translated_text_name = translate_text(name_to_translate, target_language)

        # 메뉴 번역
        translated_text_menu = []
        # 1. 리스트이면
        if type(menu_to_translate) == list:
            # 2. 하나씩 꺼내서 
            for a in menu_to_translate:
                # 3. 번역하도록 요청한다.
                translate_response_menu = translate_text(a, target_language)
                # 4. append를 써줘서 리스트에 추가한다.
                translated_text_menu.append(translate_response_menu)

        # 1. 딕셔너리면
        translated_text_price = {}
        if type(price_to_translate) == dict:
            # 2. dictionary에서 items 함수를 써줘서 하나씩 꺼낸다.
            for key, value in price_to_translate.items():
                # 3. 번역하도록 요청한다.
                translate_response_price = translate_text(key, target_language)
                # 4. dictionary[key]=value 형식으로 딕셔너리에 추가한다.
                translated_text_price[translate_response_price] = value

        translated_store = {}
        translated_store["name"]=translated_text_name
        translated_store["menu"]=translated_text_menu
        translated_store["price"]= translated_text_price

        return translated_store
    else:
        return None


@app.route('/test', methods=['POST'])
@log_function_execution_time
def api_test(store_name):
    store_info = get_store_info(store_name)
    translated_name = translate_store_info(store_info, target_language='en')
    price_list = list(translated_name.get("price",{}).values())
    updated_data = replace_price_values(translated_name, ex_list(price_list))
    return updated_data, 200

app.run(host="localhost",port=5001)