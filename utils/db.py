from pymongo import MongoClient

# MongoDB 클라이언트 생성
mongo_client = MongoClient("localhost", 27017)

# "omnivore" 데이터베이스 선택
omnivore_db = mongo_client["omnivore"]
# "store" 컬렉션 선택
store_collection = omnivore_db["store"]

log_db=mongo_client['log']
time_collection = log_db['time']


def get_store_info(store_name):
    # MongoDB에서 가게 이름에 해당하는 데이터 조회
    store_info = store_collection.find_one({"name": store_name})
    return store_info