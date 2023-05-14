import boto3
from multiprocessing import Pool

from dependency_injector.wiring import Provide, inject
from flask import render_template, request

from photo_s3_bucket.container import Container
from photo_s3_bucket.libs.image_lister import ImageLister


@inject
def generate_link_for(
    image,
    thumbnails_image_lister: ImageLister = Provide[Container.thumbnails_image_lister],
):
    photo_name= image["photo_name"]
    return {
        "name":photo_name,
        "thumbnail_url": thumbnails_image_lister.get_presigned_url(photo_name),
    }


def gallery_segment():
    TABLE_NAME = "alorenzi-pictures-votes"
    LIMIT = 10
    last_key = request.args.get("last_key", None)

    table = boto3.resource("dynamodb").Table(TABLE_NAME)

    if last_key is None:
        response = table.scan(Limit=LIMIT)
    else:
        esk = {'photo_name': last_key}
        response = table.scan(Limit=LIMIT, ExclusiveStartKey=esk)
    

    with Pool(processes=5) as p:
        images = p.map(generate_link_for, response["Items"])

    return render_template(
        "gallery_segment.html",
        images=images,
    )
