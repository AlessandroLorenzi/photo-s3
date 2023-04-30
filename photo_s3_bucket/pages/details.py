from photo_s3_bucket.libs.image_lister import ImageLister


import boto3
from flask import render_template, request

def details():
    
    s3_client = boto3.client('s3')
    image_lister = ImageLister(s3_client, 'alorenzi-pictures-backup')
    thumbnails_image_lister = ImageLister(s3_client, 'alorenzi-pictures-thumbnails')

    photo_name = request.args.get('photo', '')
    thumbnail_url = thumbnails_image_lister.get_presigned_url(photo_name)
    full_url = image_lister.get_presigned_url(photo_name)
    parent_folder = "/".join(photo_name.split('/')[:-1])+ "/"


    return render_template(
        "details.html",
        parent_folder=parent_folder,
        thumbnail_url=thumbnail_url,
        full_url=full_url,
        name= photo_name,
        vote = 3,
        tags = ['tag1', 'tag2', 'tag3'],
        )