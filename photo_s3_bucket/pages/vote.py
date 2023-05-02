from photo_s3_bucket.libs.image_lister import ImageLister


import boto3
from flask import render_template, request

from photo_s3_bucket.libs.rating import Rating

TABLE_NAME='alorenzi-pictures-test'


def vote():
    dynamodb_client = boto3.client('dynamodb', region_name='eu-south-1')
    rating_svc = Rating(dynamodb_client, TABLE_NAME)

    photo = request.args.get('photo', '')
    set_rating = request.args.get('set_rating', False)
    if set_rating:
        rating_svc.set_rating(photo, int(set_rating))

    rating = rating_svc.get_rating(photo)

    return render_template(
        "vote.html",
        rating = rating,
        name = photo,
    )
