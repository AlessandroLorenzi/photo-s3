#!/bin/env python3
import boto3

from photo_s3_bucket.libs.image_lister import ImageLister
from photo_s3_bucket.libs.thumbnailizer import Thumbnailizer


if __name__ == "__main__":
    s3_client = boto3.client("s3")
    image_lister = ImageLister(s3_client, "alorenzi-pictures-backup")
    thumbnails_image_lister = ImageLister(s3_client, "alorenzi-pictures-thumbnails")

    thumbnailizer = Thumbnailizer(
        (500, 500),
        image_lister,
        thumbnails_image_lister,
    )
    for image in thumbnailizer.image_lister.list_images_all("2021/"):
        thumbnailizer.generate(image)
