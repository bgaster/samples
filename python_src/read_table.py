import boto3
from boto3.dynamodb.conditions import Key, Attr

database_region = 'eu-west-2'
database_table = 'Samples'

dynamodb = boto3.resource('dynamodb',region_name=database_region)         

def query_unread(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name=database_region)

    table = dynamodb.Table(database_table)

    response = table.scan(
        ProjectionExpression='#ts, #vs',
        ExpressionAttributeNames={'#ts': 'timestamp', '#vs': 'values'},
        FilterExpression=Attr('read').eq(False)
    )

    return response['Items']

resp = query_unread(dynamodb)

# print(resp)

for x in resp:
    print(x)
