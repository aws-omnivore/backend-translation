from flask import request
from datetime import datetime

from utils.db import time_collection
from utils.auth import token_decode

def log_function_execution_time(func):  # func : api_test, 데코레이터로 log_function_execution_time 함수를 실행하였으므로 매개변수로 api_test를 가져온다.
    def wrapper():
        headers = request.headers
        body = request.get_json() # body 꺼내오는 함수
        # jwt decode
        decoded_dict = token_decode(headers)

        result = func(body["store_name"]) # api_test 함수 실행

        #현재 년월일시분초를 가져와서 로그에 추가
        current_time = datetime.now()

        #로그를 mongoDB에 저장
        log_entry = {
            "timestamp": current_time,
            "store_name": body["store_name"], # request body
            "translate_name": result[0]["name"], # response
            "email" : decoded_dict['email'] # auth email
        }
        time_collection.insert_one(log_entry)
     
        return result
    
    return wrapper