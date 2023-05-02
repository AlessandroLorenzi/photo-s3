import boto3
from dependency_injector import containers, providers

from photo_s3_bucket.libs.image_lister import ImageLister
from photo_s3_bucket.libs.rating import Rating
from photo_s3_bucket.libs.tags_service import TagsService
from photo_s3_bucket.libs.thumbnailizer import Thumbnailizer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    dynamodb_client = providers.Singleton(
        boto3.client,
        "dynamodb",
    )
    s3_client = providers.Singleton(
        boto3.client,
        "s3",
    )

    image_lister = providers.Singleton(
        ImageLister,
        s3_client,
        "alorenzi-pictures-backup",
    )

    thumbnails_image_lister = providers.Singleton(
        ImageLister,
        s3_client,
        "alorenzi-pictures-thumbnails",
    )

    thumbnailizer = providers.Singleton(
        Thumbnailizer,
        size=(500, 500),
        image_lister=image_lister,
        thumbnails_image_lister=thumbnails_image_lister,
    )

    rating_svc = providers.Singleton(
        Rating,
        dynamodb_client,
        "alorenzi-pictures-votes",
    )

    tags_svc = providers.Singleton(
        TagsService,
        dynamodb_client,
        "alorenzi-pictures-tags",
    )
