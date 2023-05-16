from dependency_injector.wiring import Provide, inject
from flask import render_template, request

from photo_s3_bucket.container import Container
from photo_s3_bucket.libs.image_lister import ImageLister
from photo_s3_bucket.libs.rating import Rating
from photo_s3_bucket.repositories.photo import PhotoRepository


@inject
def details(
    photo_repository: PhotoRepository = Provide[Container.photo_repository],
):
    photo_name = request.args.get("photo", "")
    photo = photo_repository.get_by_path(photo_name)    
    thumbnail_url = f"http://127.0.0.1:5000/photos/thumbnails/{photo.path}"
    full_url = f"http://127.0.0.1:5000/photos/thumbnails/{photo.path}"


    return render_template(
        "details.html",
        parent_folder="",
        thumbnail_url=thumbnail_url,
        full_url=full_url,
        photo=photo,
    )
