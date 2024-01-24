import boto3

dynamodb = boto3.resource('dynamodb',region_name='ap-northeast-2', aws_access_key_id='accesskey',aws_secret_access_key='secretkey')

table = dynamodb.Table('upbit')
data = {'가게 이름':'김밥 천국', '번호':01033071406, '메뉴':}
table.put_item(Item=data)