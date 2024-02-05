import json
from utils.logger import logged
import boto3

secret_name = "secret/aws"
region_name = "ap-northeast-2"
table_name = "exchange_late"
session = boto3.session.Session()
client = session.client(service_name='secretsmanager',region_name=region_name)
get_secret_value_response = client.get_secret_value(SecretId=secret_name)
secret = json.loads(get_secret_value_response['SecretString'])

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2', aws_access_key_id = secret["aws.accessKey"], aws_secret_access_key = secret["aws.secretKey"])


@logged
def exchange(price, target_language):
    table = dynamodb.Table("exchange_late")
    # DynamoDB에서 항목 조회
    response = table.get_item(
        Key={
            'id': '1'
        }
    )
    item = response.get('Item')
    late = float(item.get(target_language))
    return round(float(price) * late, 2)