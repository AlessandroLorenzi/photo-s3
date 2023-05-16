from dependency_injector.wiring import Provide, inject
from flask import render_template, request

from photo_s3_bucket.container import Container
from photo_s3_bucket.repositories.tag import TagRepository

HTML_TEMPLATE = "tags.html"


@inject
def get_tags(
    tag_repository: TagRepository = Provide[Container.tag_repository],
):
    photo = request.args.get("photo")

    return render_template(
        HTML_TEMPLATE,
        tags=tag_repository.get_by_path(photo),
        name=photo,
    )


@inject
def delete_tag(
    tag_repository: TagRepository = Provide[Container.tag_repository],
):
    photo = request.args.get("photo")
    tag = request.args.get("tag")

    tag_repository.delete(photo, tag)

    return render_template(
        HTML_TEMPLATE,
        tags=tag_repository.get_by_path(photo),
        name=photo,
    )


@inject
def add_tag(
    tag_repository: TagRepository = Provide[Container.tag_repository],
):
    photo = request.args.get("photo")
    tag = request.form.get("tag")
    tag_repository.create(photo, tag)

    return render_template(
        HTML_TEMPLATE,
        tags=tag_repository.get_by_path(photo),
        name=photo,
    )
