from pymongo import MongoClient
import boto3
from forex_python.converter import CurrencyRates
import time
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# MongoDB 클라이언트 생성
mongo_client = MongoClient("localhost", 27017)
# "omnivore" 데이터베이스 선택
db = mongo_client["menu"]
# "store" 컬렉션 선택
collection = db["sample"]

aws_access_key_id = os.environ.get('aws_access_key_id')
aws_secret_access_key = os.environ.get('aws_secret_access_key')

# Amazon Translate 클라이언트 생성
translate_client = boto3.client('translate', region_name='ap-northeast-2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
def get_store_info(store_name):
    # MongoDB에서 가게 이름에 해당하는 데이터 조회
    store_info = collection.find_one({"name": store_name})
    return store_info

nation_dic = {'eng': 'USD', 'jp': 'JPY'}


#함수 실행 시간 로그에 담기
def log_function_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time=time.time()
        #execution_time = end_time - start_time #함수가 실행되는 데 걸린 시간
        
        #현재 년월일시분초를 가져와서 로그에 추가
        current_time = datetime.now()

        db=mongo_client['log']
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

@log_function_execution_time
def translate_store_info(store_info:dict, target_language='en'): 
    if store_info:
        # 가게 정보에서 번역 대상 텍스트 추출 (이 예제에서는 'name' 필드를 번역합니다)
        name_to_translate = store_info.get('name', '') #가게이름
        category_to_translate=store_info.get('category', '') #카테고리 번역
        operation_to_translate= store_info.get('operation', '')
        menu_to_translate = [menu.get('name', '') for menu in store_info.get('menus', [])] #메뉴이름
        description_to_translate = [menu.get('description', '') for menu in store_info.get('menus', [])] #메뉴 설명
        price_to_translate = [menu.get('price', '') for menu in store_info.get('menus', [])] #가격
        #menu_to_translate = store_info.get('menus', '')
        #price_to_translate = store_info.get('price', '')


        # Amazon Translate를 사용하여 텍스트 번역

        #가게명 번역
        translate_response_name = translate_client.translate_text(
            Text= name_to_translate,
            SourceLanguageCode='ko',  # 가게 이름이 한국어로 되어 있다고 가정
            TargetLanguageCode=target_language
        )
        translated_text_name = translate_response_name['TranslatedText']

        #가게 카테고리 번역
        translate_response_category = translate_client.translate_text(
            Text= category_to_translate,
            SourceLanguageCode='ko',
            TargetLanguageCode=target_language
        )
        translated_text_category = translate_response_category['TranslatedText']


        # 운영시간 및 메뉴 메뉴 번역
        translated_text_operation=[]
        translated_text_menu = []
        translated_text_description=[]
        translated_text_price=[]

        # 1. 리스트이면
        if type(menu_to_translate) == list:
            # 2. 하나씩 꺼내서
            for a in menu_to_translate:
                # 3. 번역하도록 요청한다.
                translate_response_menu = translate_client.translate_text(
                    Text= a,
                    SourceLanguageCode='ko',  # 메뉴가 한국어로 되어 있다고 가정
                    TargetLanguageCode=target_language
                )
                # 4. append를 써줘서 리스트에 추가한다.
                translated_text_menu.append(translate_response_menu['TranslatedText'])
            for a in description_to_translate:
                # 3. 번역하도록 요청한다.
                translate_response_description = translate_client.translate_text(
                    Text= a,
                    SourceLanguageCode='ko',  # 메뉴가 한국어로 되어 있다고 가정
                    TargetLanguageCode=target_language
                )
                # 4. append를 써줘서 리스트에 추가한다.
                translated_text_description.append(translate_response_description['TranslatedText'])

            # for a in operation_to_translate:
            #     # 3. 번역하도록 요청한다.
            #     print("111111111111111111")
            #     translate_response_operation = translate_client.translate_text(
            #         Text= a,
            #         SourceLanguageCode='ko',  # 메뉴가 한국어로 되어 있다고 가정
            #         TargetLanguageCode=target_language
            #     )
            #     # 4. append를 써줘서 리스트에 추가한다.
            #     translated_text_operation.append(translate_response_operation['TranslatedText'])
            #     print("222222222222222222222")
                
        # 1. 딕셔너리면
        translated_text_price = {}
        if type(price_to_translate) == dict:
            # 2. dictionary에서 items 함수를 써줘서 하나씩 꺼낸다.
            for key, value in price_to_translate.items():
                # 3. 번역하도록 요청한다.
                translate_response_price = translate_client.translate_text(
                    Text= key,
                    SourceLanguageCode='ko',  # 가격이 한국어로 되어 있다고 가정
                    TargetLanguageCode=target_language
                )
                
                # 4. dictionary[key]=value 형식으로 딕셔너리에 추가한다.
                translated_text_price[translate_response_price['TranslatedText']]=value
        
        translated_store = {'name': translated_text_name, 'category': translated_text_category}
        menu_list = []
        oper_list = []
        for i in range(len(translated_text_menu)):
            menu_dict = {
                'menu': translated_text_menu[i],
                'price': price_to_translate[i],
                'description': translated_text_description[i]
            }
            menu_list.append(menu_dict)

        translated_store['menus'] = menu_list

        # for i in range(len(translated_text_operation)):
        #     oper_dict = {
        #         'operation': translated_text_menu[i],
        #         'price': price_to_translate[i],
        #         'description': translated_text_description[i]

        #     }
        #     oper_list.append(oper_dict)

        # translated_store['operation'] = menu_list
            
        translated_store["operation"] = operation_to_translate
        return translated_store #이게 이제 딕셔너리 두 개 담긴 리스트


    else:
        return None
    

def transltate_aws(text, from_lan="ko", to_lan="en"):
    #print("in transltate_aws", text)
    translate_response_operation = translate_client.translate_text(
        Text = text,
        SourceLanguageCode=from_lan,  # 메뉴가 한국어로 되어 있다고 가정
        TargetLanguageCode=to_lan
    )
    
    # print(" Translated in transltate_aws", translate_response_operation)
    return translate_response_operation["TranslatedText"]

def translate_days(operations : list, from_lan="ko", to_lan="en"):
    '''
    Describe : 운영하는 부분의 리스트를 넣으면 월요일 -> monday로 번역 되어서 추출
    Input : 
        [
            {
            "월": "10-20"
            },
            {
            "화": "11-21"
            }
        ],
    output:
        [
            {
            "monday": "10-20"
            },
        ],
    '''
    translated_operations = []
    days = [list(oneday.keys())[0] for oneday in operations]
    for i, day in enumerate(days):
        transltated_day_time = {}    
        transltated_day = transltate_aws(day,from_lan, to_lan)
        transltated_day_time[transltated_day] = operations[i][day]
        translated_operations.append(transltated_day_time)
    return translated_operations

def exchange(price, from_nation = "KRW", to_nation = "USD"):
    c = CurrencyRates()
    exchange_rate_from_to = c.get_rate(nation_dic.get(to_nation),from_nation)
    exchange_rate_from_to
    ex_result = round(price / exchange_rate_from_to, 2)
    return ex_result

def exchange_price(store : dict):
    '''
        Describe : 가게 정보 전부를 받아서 메뉴 부분만 다시 환율을 적용해서 가격을 변경 후 리턴
        Input : 번역이 된 가게의 모든 정보들 dict 폼이다.
        Output : 번역이 된 가게의 모든 정보들과 환율 적용된 메뉴의 가격이 적혀있다.
    '''
    exchange_store = store
    new_menus = []
    for menu in store["menus"]:
        new_menu = {}
        exchange_price = exchange(menu["price"])
        new_menu["menu"] = menu["menu"]
        new_menu["price"] = exchange_price
        new_menu["description"] = menu["description"]
        new_menus.append(new_menu)
    exchange_store["menus"] = new_menus

    return exchange_store
    
store_name = "스시히또"
store_info = get_store_info(store_name)

price_list=[]    
if store_info:
    # 가격 빼고 다른 설명과 가게의 이름 그리고 메뉴의 한글들을 영어로 변경
    restaurant = translate_store_info(store_info)

    # 가격 부분을 환율이 적용된 가격으로 변경 후 리턴
    restaurant = exchange_price(restaurant)

    # 요일 변경 해주는 부분
    restaurant["operation"] = translate_days(restaurant["operation"])

    print(restaurant)
else:
    print(f"{store_name}에 해당하는 가게 정보가 없습니다.")
