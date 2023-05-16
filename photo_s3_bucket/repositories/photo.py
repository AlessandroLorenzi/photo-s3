import datetime
from sqlalchemy.orm import Session

from photo_s3_bucket.models.photo import Photo


class PhotoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_path(self, path: str) -> Photo:
        return self.session.query(Photo).filter_by(path=path).first()

    def create(self, name: str, path: str, date_taken: datetime.datetime) -> Photo:
        photo = Photo(name=name, path=path, date_taken=date_taken)
        self.session.add(photo)
        self.session.commit()
        return photo

    def update(
        self, photo: Photo, name: str, path: str, date_taken: datetime.datetime
    ) -> Photo:
        photo.name = name
        photo.path = path
        photo.date_taken = date_taken
        self.session.commit()
        return photo

    def delete(self, photo: Photo):
        self.session.delete(photo)
        self.session.commit()
