import boto3

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

class TestRating:
    def setup_method(self):
        boto3.setup_default_session(profile_name='alorenzi', region_name='eu-south-1')
        self.dynamodb_client = boto3.client('dynamodb')
        self.rating = Rating(self.dynamodb_client, TABLE_NAME)
    
    def test_set_rating(self):
        self.rating.set_rating('test.jpg', 5)
        assert self.rating.get_rating('test.jpg') == 5

    
    def test_get_rating(self):
        assert self.rating.get_rating('test.jpg') == 5

    def test_get_all_5_stars(self):
        assert len(self.rating.get_photos_by_rating(5)) == 1

    def test_get_all_4_plus_stars(self):
        self.rating.set_rating('test_4.jpg', 4)
        self.rating.set_rating('test_3.jpg', 3)
        assert len(self.rating.get_photos_by_rating(4)) == 2

    def test_get_rating_not_found(self):
        assert self.rating.get_rating('FOO.JPG') == 0