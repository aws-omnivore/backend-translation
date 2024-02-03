import boto3
import sys
import json

from utils.logger import logged

secret_name = "secret/aws"
region_name = "ap-northeast-2"
# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(service_name='secretsmanager',region_name=region_name)
get_secret_value_response = client.get_secret_value(SecretId=secret_name)

secret = json.loads(get_secret_value_response['SecretString'])
# session = boto3.session.Session()
# secret_client = session.client(service_name='secretsmanager', region_name = region_name)

# # Amazon Translate 클라이언트 생성
# # translate_client = boto3.client('translate', region_name='ap-northeast-2', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
# # secret_client = boto3.client('secretsmanager', region_name=region_name)
# get_secret_value_response = secret_client.get_secret_value(SecretId=secret_name)

# secrets = get_secret_value_response['SecretString']

translate_client = boto3.client('translate', region_name='ap-northeast-2', aws_access_key_id = secret["aws.accessKey"], aws_secret_access_key = secret["aws.secretKey"])

# 매개변수로 넘어온 텍스트를 반환한다.
@logged
def translate_text(text, target_language):
    translate_response = translate_client.translate_text(
        Text= text, 
        SourceLanguageCode='ko',  # 가게 이름이 한국어로 되어 있다고 가정
        TargetLanguageCode=target_language
    )
    return translate_response['TranslatedText']