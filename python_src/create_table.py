import boto3

dynamodb = boto3.resource('dynamodb',region_name='eu-west-2')

table = dynamodb.create_table(
    TableName='Samples',
    KeySchema=[
        {
            'AttributeName': 'timestamp',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'timestamp',
            'AttributeType': 'N'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)