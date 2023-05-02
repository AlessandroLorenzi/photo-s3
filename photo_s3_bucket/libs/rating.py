TABLE_NAME='alorenzi-pictures-test'


class Rating:
    def __init__(self, dynamodb_client, table_name):
        self.dynamodb_client = dynamodb_client
        self.table_name = table_name

    def set_rating(self, photo_name, rating):
        self.dynamodb_client.put_item(
            TableName=self.table_name,
            Item={
                'photo_name': {
                    'S': photo_name,
                },
                'rating': {
                    'N': str(rating),
                },
            },
        )

    def get_rating(self, photo_name):
        response = self.dynamodb_client.get_item(
            TableName=self.table_name,
            Key={
                'photo_name': {
                    'S': photo_name,
                },
            },
        )
        if 'Item' not in response:
            return 0

        return int(response['Item']['rating']['N'])

    def get_photos_by_rating(self, rating):
        response = self.dynamodb_client.scan(
            TableName=TABLE_NAME,
            ScanFilter={
                'rating': {
                    'AttributeValueList': [
                        {
                            'N': str(rating),
                        },
                    ],
                    'ComparisonOperator': 'GE',
                },
            },
        )
        return response['Items']