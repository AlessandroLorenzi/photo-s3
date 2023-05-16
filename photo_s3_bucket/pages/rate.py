from dependency_injector.wiring import Provide, inject
from flask import render_template, request

from photo_s3_bucket.container import Container
from photo_s3_bucket.repositories.rate import RateRepository


@inject
def get_rating(
    rate_repository: RateRepository = Provide[Container.rate_repository],
):
    photo = request.args.get("photo")
    rating = rate_repository.get_by_path(photo)
    if rating:
        rating = rating.rate
    else:
        rating = 0

    return render_template(
        "vote.html",
        rating=rating,
        name=photo,
    )


@inject
def update_rating(
    rate_repository: RateRepository = Provide[Container.rate_repository],
):
    photo = request.args.get("photo")
    rating =  int(request.args.get("set_rating"))
    rate_repository.create_or_update(photo, rating)


    return render_template(
        "vote.html",
        rating=rating,
        name=photo,
    )
