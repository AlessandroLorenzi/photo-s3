from functools import lru_cache

import boto3
import botocore.exceptions
from cachetools import TTLCache, cached


class ImageLister:
    def __init__(
        self,
        s3_client: boto3.client,
        bucket_name: str,
    ):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    @lru_cache
    def list_images(self, folder: str):
        images = self.list_objects(folder)
        contents = self.filter_images(images.get("Contents", {}))
        return [content["Key"] for content in contents]

    @lru_cache
    def list_images_all(self, folder: str):
        images = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=folder)
        contents = self.filter_images(images.get("Contents", {}))
        return [content["Key"] for content in contents]

    def filter_images(self, contents: list):
        images = []
        for content in contents:
            object_metadata = self.get_metadata(content["Key"])
            if object_metadata["ContentType"].startswith("image/"):
                images.append(content)
        return images

    @lru_cache
    def is_image(self, object_path: str) -> bool:
        object_metadata = self.get_metadata(object_path)
        return object_metadata["ContentType"].startswith("image/")

    @lru_cache
    def list_subdirs(self, folder: str):
        subdirs = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name, Prefix=folder, Delimiter="/"
        )
        common_prefixes = subdirs.get("CommonPrefixes", {})
        return [prefix["Prefix"] for prefix in common_prefixes]

    @cached(cache=TTLCache(maxsize=1024, ttl=int(3600 * 0.8)))
    def get_presigned_url(self, image: str) -> str:
        PRESIGNED_URL_EXPIRATION = 3600
        url = self.s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": image,
            },
            ExpiresIn=PRESIGNED_URL_EXPIRATION,
        )
        return url

    @lru_cache
    def image_exists(self, image: str) -> bool:
        try:
            self.get_metadata(image)
            return True
        except botocore.exceptions.ClientError:
            return False

    @lru_cache
    def list_objects(self, folder: str):
        return self.s3_client.list_objects_v2(
            Bucket=self.bucket_name, Prefix=folder, Delimiter="/"
        )

    @lru_cache
    def get_object(self, object: str) -> dict:
        return self.s3_client.get_object(
            Bucket=self.bucket_name,
            Key=object,
        )

    def put_object(self, objec_patht: str, body: bytes) -> dict:
        return self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=objec_patht,
            Body=body,
        )

    @lru_cache
    def get_metadata(self, object: str) -> dict:
        return self.s3_client.head_object(
            Bucket=self.bucket_name,
            Key=object,
        )
