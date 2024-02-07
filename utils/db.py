from pymongo import MongoClient
from setting import DB_HOST, STORE_DB, STORE_COLLECTION, LOG_DB, LOG_COLLECTION

# MongoDB 클라이언트 생성
mongo_client = MongoClient(DB_HOST, 27017)
# "omnivore" 데이터베이스 선택
omnivore_db = mongo_client[STORE_DB]
# "store" 컬렉션 선택
store_collection = omnivore_db[STORE_COLLECTION]

log_db=mongo_client[LOG_DB]
time_collection = log_db[LOG_COLLECTION]


def get_store_info(store_name):
    # MongoDB에서 가게 이름에 해당하는 데이터 조회
    store_info = store_collection.find_one({"name": store_name})
    return store_info