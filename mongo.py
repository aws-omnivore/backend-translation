from pymongo import MongoClient

# MongoDB 클라이언트 생성
mongo_client = MongoClient("localhost", 27017)

# "omnivore" 데이터베이스 선택
db = mongo_client["omnivore"]

# "store" 컬렉션 선택
collection = db["store"]

def get_store_info(store_name):
    # MongoDB에서 가게 이름에 해당하는 데이터 조회
    store_info = collection.find_one({"name": store_name})

    return store_info

# 가게 이름
store_name = "김밥천국"

# 가게 정보 가져오기
store_info = get_store_info(store_name)

if store_info:
    print(store_info)
else:
    print(f"{store_name}에 해당하는 가게 정보가 없습니다.")
