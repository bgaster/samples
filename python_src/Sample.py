import boto3
from boto3.dynamodb.conditions import Key, Attr

class Sample:
    database_region = 'eu-west-2'
    database_table = 'Samples'

    def __init__(self): 
        self.dynamodb = boto3.resource('dynamodb',region_name='eu-west-2')
        self.table = self.dynamodb.Table('Samples')

    # validates a json string that it contains a valid sample
    # returns either None (if fails), otherwise a valid sample as dict
    def make_sample(self, sample):
        try:
            # sample = json.loads(data)

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
    def write(self, sample):
        self.table.put_item(
            Item={
                'timestamp': sample['timestamp'],
                'values': sample['values'],
                'read': False,
            })

    # read all unread records
    def query_unread(self):
        response = self.table.scan(
            ProjectionExpression='#ts, #vs',
            ExpressionAttributeNames={'#ts': 'timestamp', '#vs': 'values'},
            FilterExpression=Attr('read').eq(False)
        )

        return response['Items']

    # mark record as read, given timestamp
    def mark_read(self, timestamp, value=True):
        self.table.update_item(
            Key={
                    'timestamp': int(timestamp),
            },
            ExpressionAttributeNames={'#re': 'read'},
            UpdateExpression="set #re = :g",
            ExpressionAttributeValues={
                    ':g': value
                },
            ReturnValues="UPDATED_NEW"
            )

    # delete record
    def delete(self, timestamp):
        self.table.delete_item(
            Key={
                'timestamp': int(timestamp),
            },
            )