import boto3
import json
import json

secret_name = "secret/aws"
region_name = "ap-northeast-2"
# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(service_name='secretsmanager',region_name=region_name)
get_secret_value_response = client.get_secret_value(SecretId=secret_name)
secret = json.loads(get_secret_value_response['SecretString'])

mongodb_sw = False
dynamodb = boto3.client('dynamodb', region_name='ap-northeast-2', aws_access_key_id = secret["aws.accessKey"], aws_secret_access_key = secret["aws.secretKey"])

table_name = "restaurant"    # 나중에 table_name 바꾸면 수정해주기.
def get_restaurants():
    # 테이블 스캔하여 모든 아이템 가져오기
    response = dynamodb.scan(TableName=table_name)
    # items = response['Items'] if mongodb_sw else response['Items'][0]
    return response['Items']

def find_restaurant(restaurant_name: str) -> dict or None:
    if not mongodb_sw:
        items = get_restaurants()
        for item in items:
            if type(item) == dict and "name" in item:
                if type(item["name"]) == dict and item["name"].get("S", "") == restaurant_name:
                    return item
    return None
    
