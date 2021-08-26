from decimal import Decimal
import json
import boto3

database_region = 'eu-west-2'
database_table = 'Samples'

# validates a json string that it contains a valid sample
# returns either None (if fails), otherwise a valid sample as dict
def make_sample(data):
    try:
        sample = json.loads(data)

        if "timestamp" in sample and "values" in sample:
            if type(sample['timestamp']) != int:
                return None

            if not all(isinstance(n, str) for n in sample['values']) and len(sample['values']):
                return None

            sample['timestamp'] = int(sample['timestamp'])
            return sample
        else:
            return None
    except ValueError:
        return None

# writes a sample
# expects a valid sample, does not check that it is valid
def write_sample(sample, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name='eu-west-2')

    table = dynamodb.Table('Samples')

    table.put_item(
        Item={
            'timestamp': sample['timestamp'],
            'values': sample['values'],
            'read': False,
        })

# reads all samples not marked as read
# returns a list of samples that are marked as unread, could be empty
def read_samples(dynamodb=None):
    if not dynamodb:
            dynamodb = boto3.resource('dynamodb',region_name='eu-west-2')

    table = dynamodb.Table('Samples')

    response = table.scan(
        ProjectionExpression='#ts, #vs',
        ExpressionAttributeNames={'#ts': 'timestamp', '#vs': 'values'},
        FilterExpression=Attr('read').eq(False)
    )

    return response['Items']


#-----------------------------------------------------------------------

t  =  {
    'timestamp': 4,
    'values': ["1.2", "1.3", "2.4", "0.0", "0.4", "0.5", "0.7", "0.9"],
}

j = json.dumps(t)

sample = make_sample(j)

if sample == None:
    print("Invalid data")

dynamodb = boto3.resource('dynamodb',region_name='eu-west-2')
table = dynamodb.Table('Sound')

print(table.creation_date_time)
attrs = table.attribute_definitions
print(attrs)

print(sample)


write_sample(sample, dynamodb)
