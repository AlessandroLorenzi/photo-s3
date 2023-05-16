import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session

from photo_s3_bucket.models.exif import Exif


class ExifRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_path(self, path: str) -> Exif:
        return self.session.query(Exif).filter_by(path=path).first()

    def create(
        self,
        path: str,
        model: str,
        make: str,
        iso: int,
        aperture: float,
        shutter_speed: float,
        exposure_bias: float,
        exposure_program: int,
        rotation: int,
        date_taken: datetime.datetime,
    ) -> Exif:
        exif = Exif(
            path=path,
            model=model,
            make=make,
            iso=iso,
            aperture=float(aperture),
            shutter_speed=float(shutter_speed),
            exposure_bias=float(exposure_bias),
            exposure_program=exposure_program,
            rotation=rotation,
            date_taken=date_taken,
        )
        self.session.add(exif)
        self.session.commit()

    def update(
        self,
        exif: Exif,
        model: str,
        make: str,
        iso: int,
        aperture: float,
        shutter_speed: float,
        exposure_bias: float,
        exposure_program: int,
        rotation: int,
        date_taken: datetime.datetime,
    ) -> Exif:
        exif.model = model
        exif.make = make
        exif.iso = iso
        exif.aperture = aperture
        exif.shutter_speed = shutter_speed
        exif.exposure_bias = exposure_bias
        exif.exposure_program = exposure_program
        exif.rotation = rotation
        exif.date_taken = date_taken
        self.session.commit()
        return exif

    def delete(self, exif: Exif):
        self.session.delete(exif)
        self.session.commit()
