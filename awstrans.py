from flask import Flask

from setting import API_HOST
from utils.logger import log_function_execution_time
from utils.db import get_store_info
from utils.exchange_money import exchange_str_price
from utils.aws_trans import translate_text

app = Flask(__name__)

def translate_store_info(store_info: dict, target_language='en'): # target_language는 유저정보 받아오는 data에 따라 바뀔 것
    translated_store = {}
    if store_info:
        # 가게 정보에서 번역 대상 텍스트 추출 (이 예제에서는 'name' 필드를 번역합니다)
        name_to_translate = store_info.get('name', '')
        category_to_translate = store_info.get('category', '')
 
        operation_to_translate = store_info.get('operation', [])
        menus_to_translate = store_info.get('menus', [])

        translated_store['name'] = translate_text(name_to_translate, target_language)
        translated_store['category'] = translate_text(category_to_translate, target_language)

        # menus_to_translate
        new_menu = []
        for menu in menus_to_translate:
            mname_to_translate = menu.get('menu_name', '')
            price_to_translate = menu.get('menu_price', '')
            info_to_translate = menu.get('menu_info', '')

            menu['menu_name'] = translate_text(mname_to_translate, target_language)
            menu['menu_price'] = exchange_str_price(price_to_translate)
            menu['menu_info'] = translate_text(info_to_translate, target_language)

            new_menu.append(menu)
        translated_store['menus'] = new_menu
        
        # operation_to_translate
        new_operation = []
        for operation in operation_to_translate:
            day, time = list(operation.items())[0]
            
            # 월, 이런식으로 오면 요일을 붙임
            new_day = day + "요일" if day in ["월", "화", "수", "목", "금", "토", "일"] else day
            new_day = translate_text(new_day)
            
            new_operation.append({
                new_day: translate_text(time)
            })
        translated_store['operation'] = new_operation

    return translated_store


@app.route('/test', methods=['POST'])
@log_function_execution_time
def api_test(store_name: str):
    store_info = get_store_info(store_name)
    translated_store = translate_store_info(store_info, target_language='en')
    return translated_store, 200

app.run(host=API_HOST, port=5001)