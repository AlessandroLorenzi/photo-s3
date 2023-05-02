from photo_s3_bucket.libs.image_lister import ImageLister
from photo_s3_bucket.libs.rating import Rating

TABLE_NAME='alorenzi-pictures-test'


import boto3
from flask import render_template, request

def details():
    dynamodb_client = boto3.client('dynamodb', region_name='eu-south-1')
    s3_client = boto3.client('s3', region_name='eu-west-1')

    image_lister = ImageLister(s3_client, 'alorenzi-pictures-backup')
    thumbnails_image_lister = ImageLister(s3_client, 'alorenzi-pictures-thumbnails')

    photo_name = request.args.get('photo', '')
    thumbnail_url = thumbnails_image_lister.get_presigned_url(photo_name)
    full_url = image_lister.get_presigned_url(photo_name)
    parent_folder = "/".join(photo_name.split('/')[:-1])+ "/"


    rating_svc = Rating(dynamodb_client, TABLE_NAME)

    rate = rating_svc.get_rating(photo_name)
    
    return render_template(
        "details.html",
        parent_folder=parent_folder,
        thumbnail_url=thumbnail_url,
        full_url=full_url,
        name= photo_name,
        rating = rate,
        tags = ['tag1', 'tag2', 'tag3'],
        )