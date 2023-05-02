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
    return {
        "name": image,
        "thumbnail_url": thumbnails_image_lister.get_presigned_url(image),
    }


@inject
def navigation(
    image_lister: ImageLister = Provide[Container.image_lister],
):
    subdir = request.args.get("folder", "")
    if subdir == "/":
        subdir = ""

    folders = image_lister.list_subdirs(subdir)

    parent_folder = "/".join(subdir.split("/")[:-2]) + "/"

    images = image_lister.list_images(subdir)

    with Pool(processes=5) as p:
        images_links = p.map(generate_link_for, images)

    return render_template(
        "navigation.html",
        images=images_links,
        folders=folders,
        parent_folder=parent_folder,
    )
