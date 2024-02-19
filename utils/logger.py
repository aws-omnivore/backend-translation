from flask import request
import logging
from datetime import datetime
import boto3
import uuid
from utils.auth import token_decode
from setting import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

logging.basicConfig(level='INFO')

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

table = dynamodb.Table('recent_log')

dynamo_mongo_sw="mongodb"

def log_function_execution_time(func):  # func : api_test, 데코레이터로 log_function_execution_time 함수를 실행하였으므로 매개변수로 api_test를 가져온다.
    def wrapper():
        headers = request.headers
        query_params = request.args
        # jwt decode
        decoded_dict = token_decode(headers)


        if dynamo_mongo_sw=="mongodb":
            response, status = func(query_params.get("name")) # api_test 함수 실행
        elif dynamo_mongo_sw=="dynamo":
            response, status = func(query_params.get("name")["S"]) # api_test 함수 실행

        #현재 년월일시분초를 가져와서 로그에 추가
        current_time = int(str(datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".",""))

        def generate_uuid():
            return uuid.uuid4()
        
        new_uuid = str(generate_uuid())
        
        restaurant_id = ""
        if response and type(response) == dict:
            restaurant_id_dict = response.get("id", {})
            restaurant_id = restaurant_id_dict#.get("S", "")

        #로그를 mongoDB에 저장
        log_entry = {
            "id": new_uuid,
            "timestamp": current_time,
            "restaurant_id": restaurant_id,  
            "name": query_params.get("name", ""), # request body       
            # "translate_name": response["name"], # response
            "email" : decoded_dict.get('email', "") # auth email
        }
        return response, status
    
    return wrapper

def logged(func, *args, **kwargs):
    logger = logging.getLogger()
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info("calling {} with args {} and kwargs {}, result is {}".format(func.__name__, args, kwargs, result))
        return result
    return wrapper