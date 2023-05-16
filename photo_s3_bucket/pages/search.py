from dependency_injector.wiring import Provide, inject
from flask import render_template, request

from photo_s3_bucket.container import Container

from multiprocessing import Pool

from photo_s3_bucket.repositories.tag import TagRepository

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
def search(
    tag_repository: TagRepository = Provide[Container.tag_repository],
):
    tag = request.args.get("tag", "")

    images = []
    if tag == "":
        return render_template(
            "search.html",
            images=[],
        )

    images = tag_repository.get_by_tag(tag)

    with Pool(processes=5) as p:
        images_links = p.map(generate_link_for, images)

    return render_template(
        "search.html",
        images=images_links,
    )
