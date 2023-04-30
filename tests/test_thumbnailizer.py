import boto3

from photo_s3_bucket.libs.image_lister import ImageLister
from photo_s3_bucket.libs.thumbnailizer import Thumbnailizer

class TestThumbnailizer:
    def setup_method(self):
        boto3.setup_default_session(profile_name='alorenzi')
        s3_client = boto3.client('s3')
        image_lister = ImageLister(s3_client, 'alorenzi-pictures-backup')
        thumbnails_image_lister = ImageLister(s3_client, 'alorenzi-pictures-thumbnails')

        self.thumbnailizer = Thumbnailizer(
            (500, 500), 
            image_lister, 
            thumbnails_image_lister, 
        )

    def test_thumbnailize(self):
        self.thumbnailizer.generate('2023/04/23/DSC06732.JPG')

    def test_thumbnailize_all(self):
        for image in self.thumbnailizer.image_lister.list_images_all('2023/04/23'):
            self.thumbnailizer.generate(image)

