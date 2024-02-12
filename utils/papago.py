import json
import urllib.request

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

    Client_ID = "vdCP1nEnOBBDS9HoBBXi"
    Client_Secret = "7ECb_RpZTx"

    encText = urllib.parse.quote(text)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",Client_ID)
    request.add_header("X-Naver-Client-Secret",Client_Secret)
    
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_body_str = response_body.decode('utf-8')
        response_body = json.loads(response_body_str)
        return response_body["message"]["result"]["translatedText"]
    else:
        print("Error Code:" + rescode)