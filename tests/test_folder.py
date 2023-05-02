from dataclasses import dataclass
from unittest.mock import MagicMock

import boto3
import httpx

from photo_s3_bucket.libs.image_lister import ImageLister


class TestImageLister:
    def setup_method(self):
        s3_client = boto3.client("s3")
        self.image_lister = ImageLister(s3_client, "alorenzi-pictures-backup")

    def test_list_images(self):
        images = self.image_lister.list_images("2023/04/26/")
        assert images[0] == "2023/04/26/DSC06818.JPG"

    def test_list_subdir(self):
        subdirs = self.image_lister.list_subdirs("2023/04/")
        assert subdirs == [
            "2023/04/02/",
            "2023/04/17/",
            "2023/04/21/",
            "2023/04/22/",
            "2023/04/23/",
            "2023/04/26/",
        ]

    def test_get_presigned_url(self):
        image = self.image_lister.get_presigned_url("2023/04/26/DSC06818.JPG")

        resp = httpx.get(image, timeout=5)
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "image/jpeg"
        assert resp.headers["content-length"] == "5865472"

    def test_image_exists(self):
        assert self.image_lister.image_exists("2023/04/26/DSC06818.JPG")

    def test_image_does_not_exist(self):
        assert not self.image_lister.image_exists("2023/04/26/DSC06818.JPG2")
