import json
from flask import Flask, request
from utils.papago import translate_with_papago

app = Flask(__name__)

@app.route("/translate/store", methods=["POST"])
def translate_store():
    body = request.get_data() # client에서 가지고온 body
    body_dict = json.loads(body) # 가지고온 body가 string이니까 이를 dictionary로 바꾸기 위해서 loads 함수를 사용한다.

    target_lang_value = body_dict['target_lang'] # target_lang은 dic'형식이니까 key값이 되고 이런 key값은 오직 1개만 가질 수 있으므로 이에 해당하는
                                           # value값을 가져올 수 있게 된다.
    text_value = body_dict['text']

    translated = translate_with_papago(target_lang=target_lang_value, text=text_value)
    return translated

app.run(host="localhost",port=5001)