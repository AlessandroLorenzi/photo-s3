import boto3

from photo_s3_bucket.libs.tags_service import TagsService


class TestTags:
    def setup_method(self):
        self.dynamodb_client = boto3.client("dynamodb")
        self.tags_service = TagsService(self.dynamodb_client, "alorenzi-pictures-tags")

    def test_set_tags(self):
        self.tags_service.set(
            "2023/04/23/DSC06729.JPG", ["populonia", "toscana", "landscape"]
        )

    def test_get_tags(self):
        assert self.tags_service.get_tags("2023/04/23/DSC06729.JPG") == [
            "landscape",
            "populonia",
            "toscana",
        ]

    def test_get_photos(self):
        assert self.tags_service.get_photos("landscape") == ["2023/04/23/DSC06729.JPG"]

    def test_add_tag(self):
        self.tags_service.add_tag("2023/04/23/DSC06729.JPG", "maremma")

    def test_drop_tag(self):
        self.tags_service.drop_tag("2023/04/23/DSC06729.JPG", "maremma")
