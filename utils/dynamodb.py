
import json
import logging
import boto3
from boto3.dynamodb.conditions import Key

from utils.logger import logged

secret_name = "secret/aws"
region_name = "ap-northeast-2"
# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(service_name='secretsmanager',region_name=region_name)
get_secret_value_response = client.get_secret_value(SecretId=secret_name)
secret = json.loads(get_secret_value_response['SecretString'])

mongodb_sw = False
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2', aws_access_key_id = secret["aws.accessKey"], aws_secret_access_key = secret["aws.secretKey"])

table_name = "restaurant"  

@logged
def find_by_restaurant_id(id: str) -> dict or None:
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={
        'id': id
    })
    item = response['Item']
    if item:
        logging.info({"request": id, "response": item})
        return item
    logging.info({"request": id, "response": None})
    return None

@logged
def find_restaurant(name: str) -> dict or None:
    table = dynamodb.Table(table_name)
    response = table.query(
        IndexName = 'name-index',
        KeyConditionExpression=Key('name').eq(name)
    )
    items = response['Items']
    if items:
        return items[0]
    return None
    
