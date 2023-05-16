from dependency_injector import containers, providers

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
