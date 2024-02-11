from flask import Flask,request
from flask_cors import CORS
from setting import API_HOST
from utils.dynamodb import find_restaurant, find_by_restaurant_id
from utils.logger import log_function_execution_time, logged
from utils.exchange_money import exchange
from utils.aws_trans import translate_text

app = Flask(__name__)

CORS(app)

mongodb_sw = False

@logged
def translate_store_info(restaurant_info: dict, target_language): 
    translated_store = restaurant_info

    if restaurant_info:
        name_to_translate = restaurant_info.get('name', '')
        category_to_translate = restaurant_info.get('category', '')
        operation_to_translate = restaurant_info.get('operation', '')
        menus_to_translate = restaurant_info.get('menus', '')

        translated_store['name'] = translate_text(name_to_translate, target_language)
        translated_store['category'] = translate_text(category_to_translate, target_language)

        transformed_menus = []
        for menu in menus_to_translate:
           
            mname_to_translate = menu.get('name', '')
            price_to_translate = menu.get('price', '')
            info_to_translate = menu.get('description', '')
        
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
    return translated_store

@app.route('/api/v1/record/<restaurant_id>', methods=['GET'])
def api_for_id(restaurant_id):
    target_language = request.headers.get("Language")
    restaurant_info_id = find_by_restaurant_id(restaurant_id)
    translated_store = translate_store_info(restaurant_info_id, target_language)

    if not translated_store:
        return "No Content", 204
    return translated_store, 200

@app.route('/api/v1/record', methods=['GET'])
@log_function_execution_time
def api_for_name(restaurant_name: str):
    target_language = request.headers.get("Language", "en")
    restaurant_info = find_restaurant(restaurant_name)
    translated_store = translate_store_info(restaurant_info, target_language) # target language는 프론트에서 header에 담겨져 온다
    if not translated_store:
        return "No Content", 204
    return translated_store, 200


app.run(host=API_HOST, port=5001)

# test