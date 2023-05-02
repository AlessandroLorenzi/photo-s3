from dependency_injector.wiring import Provide, inject
from flask import render_template, request

from photo_s3_bucket.container import Container
from photo_s3_bucket.libs.image_lister import ImageLister
from photo_s3_bucket.libs.rating import Rating


@inject
def vote(
    rating_svc: Rating = Provide[Container.rating_svc],
):
    photo = request.args.get("photo", "")

    set_rating = request.args.get("set_rating", False)
    if set_rating:
        rating_svc.set_rating(photo, int(set_rating))

    rating = rating_svc.get_rating(photo)

    return render_template(
        "vote.html",
        rating=rating,
        name=photo,
    )
