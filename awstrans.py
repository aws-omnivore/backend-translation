from flask import Flask,request
from flask_cors import CORS
from setting import API_HOST
from utils.dynamodb import find_restaurant, find_restaurant_id
from utils.logger import log_function_execution_time
from utils.db import get_store_info
from utils.exchange_money import exchange, exchange_str_price
from utils.aws_trans import translate_text

app = Flask(__name__)

CORS(app)

mongodb_sw = False


def translate_store_info(restaurant_info: dict, target_language): # target_language는 유저정보 받아오는 data에 따라 바뀔 것
    translated_store = restaurant_info

    # del translated_store["_id"] # MongoDB에는 있지만 DynamoDB에는 없는 key 값
    if restaurant_info:
        # 가게 정보에서 번역 대상 텍스트 추출 (이 예제에서는 'name' 필드를 번역합니다)
        name_to_translate = restaurant_info.get('name', '') if mongodb_sw else restaurant_info.get('name', '')
        category_to_translate = restaurant_info.get('category', '') if mongodb_sw else restaurant_info.get('category', '')
        operation_to_translate = restaurant_info.get('operation', '') if mongodb_sw else restaurant_info.get('operation', '')
        menus_to_translate = restaurant_info.get('menus', '') if mongodb_sw else restaurant_info.get('menus', '')

        translated_store['name'] = translate_text(name_to_translate, target_language)
        translated_store['category'] = translate_text(category_to_translate, target_language)

        transformed_menus = []
        for menu in menus_to_translate:
           
            mname_to_translate = menu.get('name', '') if mongodb_sw else menu.get('name', '')
            
            if mongodb_sw :
                price_to_translate = menu.get('price', '')
            else: 
                #price_NS = menu.get('price', '')
                price_to_translate = menu.get('price', '')#[list(price_NS.keys())[0]]

            info_to_translate = menu.get('description', '') if mongodb_sw else menu.get('description', '')
        
            menu['name'] = translate_text(mname_to_translate, target_language)
            menu['price'] = exchange(price_to_translate, target_language)
            menu['description'] = translate_text(info_to_translate, target_language)

            transformed_menus.append(menu)
        translated_store['menus'] = transformed_menus

        new_operation = []
        for operation in operation_to_translate:
            for day, time in operation.items():
                new_day = day + "요일" if day in ["월", "화", "수", "목", "금", "토", "일"] else day
                new_day = translate_text(new_day,target_language)
                new_operation.append({
                    new_day: translate_text(time,target_language)
                })

        translated_store['operation'] = new_operation

        # for operation in operation_to_translate:
        #     print("op: ", operation)
            
        #     if mongodb_sw:
        #         day, time = list(operation.items())[0]
        #     else:
        #         day = operation.keys()
        #         print(day)
        #         time = operation.get(day, '')
            
            # 월, 이런식으로 오면 요일을 붙임
    return translated_store

@app.route('/api/v1/record_id', methods=['POST', 'GET'])
def api_test_id():
    target_language = request.headers.get("Language")
    restaurant_id = request.args.get("restaurantId")
    restaurant_info_id = find_restaurant_id(restaurant_id)
    translated_store = translate_store_info(restaurant_info_id, target_language)

    if not translated_store:
        return "No Content", 204
    return translated_store, 200


@app.route('/api/v1/record_name', methods=['POST', 'GET'])
@log_function_execution_time
def api_test(restaurant_name: str):
    target_language = request.headers.get("Language")
    restaurant_info = find_restaurant(restaurant_name)
    translated_store = translate_store_info(restaurant_info, target_language) # target language는 프론트에서 header에 담겨져 온다

    if not translated_store:
        return "No Content", 204
    return translated_store, 200


app.run(host=API_HOST, port=5001)
