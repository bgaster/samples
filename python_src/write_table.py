from decimal import Decimal
import boto3

dynamodb = boto3.resource('dynamodb',region_name='eu-west-2')
table = dynamodb.Table('Samples')

table.put_item(
   Item={
        'timestamp': int(1),
        'values': [Decimal('1.2'), Decimal('1.3'), Decimal('2.4'), 
                   Decimal('0.0'), Decimal('0.4'), Decimal('0.5'), 
                   Decimal('0.7'), Decimal('0.9')],
        'read': False,
    }
)