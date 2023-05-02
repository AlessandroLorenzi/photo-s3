from dependency_injector.wiring import Provide, inject
from flask import render_template, request

from photo_s3_bucket.container import Container
from photo_s3_bucket.libs.image_lister import ImageLister


@inject
def navigation(
    image_lister: ImageLister = Provide[Container.image_lister],
    thumbnails_image_lister: ImageLister = Provide[Container.thumbnails_image_lister],
):
    subdir = request.args.get("folder", "")
    if subdir == "/":
        subdir = ""

    folders = image_lister.list_subdirs(subdir)
    images = image_lister.list_images(subdir)

    images_links = []
    parent_folder = "/".join(subdir.split("/")[:-2]) + "/"

    for image in images:
        images_links.append(
            {
                "name": image,
                "thumbnail_url": thumbnails_image_lister.get_presigned_url(image),
            }
        )

    return render_template(
        "navigation.html",
        images=images_links,
        folders=folders,
        parent_folder=parent_folder,
    )
