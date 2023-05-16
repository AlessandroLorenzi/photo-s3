import boto3
from multiprocessing import Pool

from dependency_injector.wiring import Provide, inject
from flask import render_template, request

from photo_s3_bucket.container import Container
from photo_s3_bucket.libs.image_lister import ImageLister
from photo_s3_bucket.repositories.photo import PhotoRepository


@inject
def generate_link_for(
    photo,
):
    photo_name = photo.path
    thumbnail_url = f"http://127.0.0.1:5000/photos/thumbnails/{photo.path}"
    return {
        "name": photo_name,
        "thumbnail_url": thumbnail_url,
    }


@inject
def gallery_segment(
    photo_repository: PhotoRepository = Provide[Container.photo_repository],
):
    page = request.args.get("page", default=0, type=int)
    photos= photo_repository.get_all(page=page)

    return render_template(
        "gallery_segment.html",
        images=[generate_link_for(photo) for photo in photos],
        next_page = page+1,
    )
