import requests

CLIENT_ID="vdCP1nEnOBBDS9HoBBXi"
CLIENT_SECRET="7ECb_RpZTx"
URL="https://openapi.naver.com/v1/papago/n2mt"
SOURCE_LANG="ko"

def translate_with_papago(target_lang, text):
    # papago api 에 요청할 데이터 셋팅
    data = f"source={SOURCE_LANG}&target={target_lang}&text={text}".encode()
    # papago api 에 요청할 때 필요한 헤더 셋팅
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Naver-Client-Id" : CLIENT_ID,
        "X-Naver-Client-Secret" : CLIENT_SECRET
    }

    # papago api에 요청
    response = requests.post(URL, data=data, headers=headers)
    response_json = response.json()   # json의 dic' 형식으로 변환한다.

    return response_json["message"]["result"]
print(translate_with_papago(target_lang="en", text="안녕"))