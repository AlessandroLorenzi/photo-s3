#!/bin/env python3
import boto3

from photo_s3_bucket.libs.image_lister import ImageLister
TABLE_NAME = "alorenzi-pictures-votes"

s3_client = boto3.client("s3")
dynamodb_client = boto3.client("dynamodb")

image_lister = ImageLister(s3_client, "alorenzi-pictures-backup")

print("Fetching images list")
images = image_lister.list_images_all("")

print("Found {} images".format(len(images)))

for image in images:
    response = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key={
            "photo_name": {
                "S": image,
            },
        },
    )
    if "Item" in response:
        print("Skipping {}".format(image))
        continue
    print("Adding {}".format(image))
    dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item={
            "photo_name": {
                "S": image,
            },
            "rating": {
                "N": "0",
            },
        },
    )
