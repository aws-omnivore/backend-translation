from pymongo import MongoClient
import time
from datetime import datetime
client=MongoClient(host='localhost',port=27017)

db=client['log']
collection = db['time']

def log_function_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time=time.time()
        #execution_time = end_time - start_time #함수가 실행되는 데 걸린 시간
        #현재 년월일시분초를 가져와서 로그에 추가
        current_time = datetime.now()
        
        db=client['log']
        collection = db['time']



        #로그를 mongoDB에 저장
        log_entry = {
            "function_name": func.__name__,
            #"execution_time": execution_time,
            "timestamp": current_time
        }
        collection.insert_one(log_entry)
        return result
    return wrapper
#데코레이터를 사용하여 함수에 적용
@log_function_execution_time
def test_func():
    print("테스트 함수")
test_func()