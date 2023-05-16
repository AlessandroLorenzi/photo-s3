import boto3
from dependency_injector import containers, providers

from photo_s3_bucket.libs.image_lister import ImageLister
from photo_s3_bucket.libs.rating import Rating
from photo_s3_bucket.libs.tags_service import TagsService
from photo_s3_bucket.libs.thumbnailizer import Thumbnailizer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from photo_s3_bucket.repositories.photo import PhotoRepository
from photo_s3_bucket.repositories.exif import ExifRepository
from photo_s3_bucket.repositories.rate import RateRepository
from photo_s3_bucket.repositories.tag import TagRepository

database_url = "postgresql://photo_bucket:photo_bucket@localhost:5432/photo_bucket"
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)


photo_repository = PhotoRepository(Session())
exif_repository = ExifRepository(Session())


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
    
    session = providers.Singleton(Session)

    photo_repository = providers.Singleton(
        PhotoRepository,
        session,
    )
    exif_repository = providers.Singleton(
        ExifRepository,
        session,
    )
    
    rate_repository = providers.Singleton(
        RateRepository,
        session,
    )

    tag_repository = providers.Singleton(
        TagRepository,
        session,
    )