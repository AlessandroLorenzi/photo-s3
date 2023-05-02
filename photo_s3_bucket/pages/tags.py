from dependency_injector.wiring import Provide, inject
from flask import render_template, request

from photo_s3_bucket.container import Container
from photo_s3_bucket.libs.tags_service import TagsService


@inject
def get_tags(
    tags_svc: TagsService = Provide[Container.tags_svc],
):
    photo = request.args.get("photo", "")

    return render_template(
        "tags.html",
        tags=tags_svc.get_tags(photo),
        name=photo,
    )


@inject
def delete_tag(
    tags_svc: TagsService = Provide[Container.tags_svc],
):
    photo = request.args.get("photo", "")
    tag = request.args.get("tag", "")

    tags_svc.drop_tag(photo, tag)

    return render_template(
        "tags.html",
        tags=tags_svc.get_tags(photo),
        name=photo,
    )


@inject
def add_tag(
    tags_svc: TagsService = Provide[Container.tags_svc],
):
    photo = request.args.get("photo", "")
    tag = request.form.get("tag", "")
    if tag != "":
        tags_svc.add_tag(photo, tag)

    print(tag)
    return render_template(
        "tags.html",
        tags=tags_svc.get_tags(photo),
        name=photo,
    )
