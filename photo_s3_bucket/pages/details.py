from dependency_injector.wiring import Provide, inject
from flask import render_template, request

from photo_s3_bucket.container import Container
from photo_s3_bucket.libs.image_lister import ImageLister
from photo_s3_bucket.libs.rating import Rating


@inject
def details(
    image_lister: ImageLister = Provide[Container.image_lister],
    thumbnails_image_lister: ImageLister = Provide[Container.thumbnails_image_lister],
    rating_svc: Rating = Provide[Container.rating_svc],
):
    photo_name = request.args.get("photo", "")
    thumbnail_url = thumbnails_image_lister.get_presigned_url(photo_name)
    full_url = image_lister.get_presigned_url(photo_name)

    parent_folder = "/".join(photo_name.split("/")[:-1]) + "/"

    rate = rating_svc.get_rating(photo_name)

    return render_template(
        "details.html",
        parent_folder=parent_folder,
        thumbnail_url=thumbnail_url,
        full_url=full_url,
        name=photo_name,
        rating=rate,
        tags=["tag1", "tag2", "tag3"],
    )
