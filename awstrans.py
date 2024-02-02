from flask import Flask
from setting import API_HOST
from utils.dynamodb import find_restaurant
from utils.logger import log_function_execution_time
from utils.db import get_store_info
from utils.exchange_money import exchange_str_price
from utils.aws_trans import translate_text

app = Flask(__name__)

mongodb_sw = False

def translate_store_info(restaurant_info: dict, target_language='en'): # target_language는 유저정보 받아오는 data에 따라 바뀔 것
    translated_store = restaurant_info

    # del translated_store["_id"] # MongoDB에는 있지만 DynamoDB에는 없는 key 값
    if restaurant_info:
        # 가게 정보에서 번역 대상 텍스트 추출 (이 예제에서는 'name' 필드를 번역합니다)
        name_to_translate = restaurant_info.get('name', '') if mongodb_sw else restaurant_info["name"].get('S', '')
        category_to_translate = restaurant_info.get('category', '') if mongodb_sw else restaurant_info["category"].get('S', '')
        operation_to_translate = restaurant_info.get('operation', '') if mongodb_sw else restaurant_info["operation"].get('L', '')
        menus_to_translate = restaurant_info.get('menus', '') if mongodb_sw else restaurant_info["menus"].get('L', '')

        translated_store['name'] = translate_text(name_to_translate, target_language)
        translated_store['category'] = translate_text(category_to_translate, target_language)

        transformed_menus = []
        for menu in menus_to_translate:
           
            mname_to_translate = menu.get('name', '') if mongodb_sw else menu["M"].get('name', '')["S"]
            
            if mongodb_sw :
                price_to_translate = menu.get('price', '')
            else: 
                price_NS = menu["M"].get('price', '')
                price_to_translate = menu["M"].get('price', '')[list(price_NS.keys())[0]]

            info_to_translate = menu.get('description', '') if mongodb_sw else menu["M"].get('description', '')["S"]
        
            menu['name'] = translate_text(mname_to_translate, target_language)
            menu['price'] = exchange_str_price(price_to_translate)
            menu['description'] = translate_text(info_to_translate, target_language)

            transformed_menus.append(menu)
        translated_store['menus'] = transformed_menus

        new_operation = []
        for operation in operation_to_translate:
            
            if mongodb_sw:
                day, time = list(operation.items())[0]
            else:
                day = list(operation["M"].keys())[0]
                time = operation["M"][day]["S"]
            
            # 월, 이런식으로 오면 요일을 붙임
            new_day = day + "요일" if day in ["월", "화", "수", "목", "금", "토", "일"] else day
            new_day = translate_text(new_day)
            
            new_operation.append({
                new_day: translate_text(time)
            })
        translated_store['operation'] = new_operation

    return translated_store

@app.route('/api/v1/record', methods=['POST'])
@log_function_execution_time
def api_test(restaurant_name: str):
    restaurant_info = find_restaurant(restaurant_name)
    translated_store = translate_store_info(restaurant_info, target_language='en') # target language는 프론트에서 header에 담겨져 온다

    if not translated_store:
        return "No Content", 204
    return translated_store, 200

app.run(host=API_HOST, port=5001)
