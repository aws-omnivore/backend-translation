import base64
import json

def token_decode(headers):
    value = headers.get("Authorization")
    v = value.split(" ")[1]

    # JWT payload 추출
    payload_encoded = v.split('.')[1]

    # Base64 디코딩
    payload_bytes = base64.urlsafe_b64decode(payload_encoded + '==')
    decoded_payload = payload_bytes.decode('utf-8')
    payload_dict = json.loads(decoded_payload)

    return payload_dict