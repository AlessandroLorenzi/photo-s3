import boto3

class TestRating:
    def test_initialize_rating(self):
        boto3.setup_default_session(profile_name='alorenzi', region_name='eu-south-1')
        dynamodb_client = boto3.client('dynamodb') 
        response = dynamodb_client.create_table(
            TableName='alorenzi-pictures-ratings',
            KeySchema=[
                {
                    'AttributeName': 'photo_name',
                    'KeyType': 'HASH',
                },
                {
                    'AttributeName': 'rating',
                    'KeyType': 'RANGE',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'photo_name',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'rating',
                    'AttributeType': 'N',
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            },
        )
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200
    
    def test_set_rating(self):
        boto3.setup_default_session(profile_name='alorenzi', region_name='eu-south-1')
        dynamodb_client = boto3.client('dynamodb')
        response = dynamodb_client.put_item(
            TableName='alorenzi-pictures-ratings',
            Item={
                'photo_name': {
                    'S': '2023/04/23/DSC06732.JPG',
                },
                'rating': {
                    'N': '5',
                },
            },
        )
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200
    
    def test_get_rating(self):
        boto3.setup_default_session(profile_name='alorenzi', region_name='eu-south-1')
        dynamodb_client = boto3.client('dynamodb')
        response = dynamodb_client.get_item(
            TableName='alorenzi-pictures-ratings',
            Key={
                'photo_name': {
                    'S': '2023/04/23/DSC06732.JPG',
                },
            },
        )
        assert response['Item']['rating']['N'] == '5'

    def test_get_all_5_stars(self):
        boto3.setup_default_session(profile_name='alorenzi', region_name='eu-south-1')
        dynamodb_client = boto3.client('dynamodb')
        response = dynamodb_client.get_item(
            TableName='alorenzi-pictures-ratings',
            Key={
                'rating': {
                    'N': '5',
                },
            },
        )
        assert response['Item'] == []
