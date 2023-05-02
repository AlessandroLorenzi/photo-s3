import boto3

from photo_s3_bucket.libs.rating import Rating

TABLE_NAME='alorenzi-pictures-test'

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