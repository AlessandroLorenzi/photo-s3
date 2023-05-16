from dependency_injector.wiring import Provide, inject
from flask import render_template, request

from photo_s3_bucket.container import Container
from photo_s3_bucket.libs.tags_service import TagsService
from photo_s3_bucket.libs.image_lister import ImageLister

from multiprocessing import Pool


@inject
def generate_link_for(
    image,
    thumbnails_image_lister: ImageLister = Provide[Container.thumbnails_image_lister],
):
    return {
        "name": image,
        "thumbnail_url": thumbnails_image_lister.get_presigned_url(image),
    }


@inject
def search(
    tags_svc: TagsService = Provide[Container.tags_svc],
):
    tag = request.args.get("tag", "")

    images = []
    if tag == "":
        return render_template(
            "search.html",
            images=[],
        )

    images = tags_svc.get_photos(tag)

    with Pool(processes=5) as p:
        images_links = p.map(generate_link_for, images)

    return render_template(
        "search.html",
        images=images_links,
    )
