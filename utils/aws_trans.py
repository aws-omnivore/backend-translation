import boto3
import os
from dotenv import load_dotenv
load_dotenv()

aws_access_key_id = os.environ.get('aws_access_key_id')
aws_secret_access_key = os.environ.get('aws_secret_access_key')

# Amazon Translate 클라이언트 생성
translate_client = boto3.client('translate', region_name='ap-northeast-2', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)


# 매개변수로 넘어온 텍스트를 반환한다.
def translate_text(text, target_language="en"):
    translate_response = translate_client.translate_text(
        Text= text, 
        SourceLanguageCode='ko',  # 가게 이름이 한국어로 되어 있다고 가정
        TargetLanguageCode=target_language
    )
    return translate_response['TranslatedText']
