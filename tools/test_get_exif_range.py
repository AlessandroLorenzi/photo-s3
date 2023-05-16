#!/usr/bin/env python


import boto3
from PIL import Image, ExifTags, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

s3 = boto3.client("s3")
obj = s3.get_object(
    Bucket="alorenzi-pictures-backup",
    Key="2023/04/26/DSC06818.JPG",
    Range="bytes=0-200",
)
photo = Image.open(obj["Body"])
print(photo._getexif())

exifs = photo.getexif()
for tag, value in exifs.items():
    decoded = ExifTags.TAGS.get(tag, tag)
    print(decoded, value)
