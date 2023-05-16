#!/bin/env python3
import glob
from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from photo_s3_bucket.models.photo import Photo
from sqlalchemy.exc import IntegrityError

from photo_s3_bucket.repositories.photo import PhotoRepository
from photo_s3_bucket.repositories.exif import ExifRepository

database_url = "postgresql://photo_bucket:photo_bucket@localhost:5432/photo_bucket"
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
SOURCE_PATH = "./test_pictures/source"
ORIGINALS_PATH = "./test_pictures/originals"
THUMBNAILS_PATH = "./test_pictures/thumbnails"

photo_repository = PhotoRepository(Session())
exif_repository = ExifRepository(Session())


class ImportImages:
    def __init__(self, source_path: str = "./test_pictures/source/**"):
        self.source_path = source_path

    def __call__(self):
        images = self.list_images_in_directory()
        errors = {}
        for image in images:
            try: 
                import_image = ImportImage(image)
                import_image()
            except Exception as e:
                errors[image] = e
        print(errors)


    def list_images_in_directory(self):
        files = glob.glob(self.source_path, recursive=True)
        images = [
            file for file in files if file.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
        return images


class ImportImage:
    def __init__(self, image_path):
        self.image_path = image_path
        self.exif = None

    def __call__(self):
        print(f"Importing image: {self.image_path}")
        if self.image_already_imported():
            print("Image already imported.")
            return

        self.get_exif_data()
        self.create_thumbnail()
        self.save_to_database()

    def image_already_imported(self):
        return photo_repository.get_by_path(self.image_path) is not None

    def get_exif_data(self):
        if self.exif is not None:
            return self.exif

        with Image.open(self.image_path) as img:
            exif_data = img._getexif()
            if exif_data is None:
                print("No EXIF data found.")
                return

            if 36867 in exif_data:
                date_taken = datetime.strptime(
                    exif_data.get(36867, None), "%Y:%m:%d %H:%M:%S"
                )
            else:
                date_taken = datetime.datetime.now()

            self.exif = {
                "Model": exif_data.get(272, None),
                "Make": exif_data.get(271, None),
                "ISO": exif_data.get(34855, None),
                "Aperture": exif_data.get(33437, None),
                "ShutterSpeed": exif_data.get(33434, None),
                "ExposureBias": exif_data.get(37380, None),
                "ExposureProgram": exif_data.get(34850, None),
                "Rotation": exif_data.get(274, None),
                "DateTaken": date_taken,
            }
        return self.exif

    def create_directory_if_not_exists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def create_thumbnail(self):
        self.get_exif_data()

        date_taken = self.exif["DateTaken"]
        file_name = self.image_path.split("/")[-1]

        image_thumbnail_path = (
            f"{THUMBNAILS_PATH}/{date_taken.year}/{date_taken.month}/{date_taken.day}/"
        )
        image_original_path = (
            f"{ORIGINALS_PATH}/{date_taken.year}/{date_taken.month}/{date_taken.day}/"
        )
        self.create_directory_if_not_exists(image_thumbnail_path)
        self.create_directory_if_not_exists(image_original_path)

        with Image.open(self.image_path) as img:
            img.save(
                f"{image_original_path}/{file_name}",
                exif=img.info["exif"],
            )
            img.thumbnail((512, 512))
            img.save(
                f"{image_thumbnail_path}/{file_name}",
                exif=img.info["exif"],
            )

    def save_to_database(self):
        date_taken = self.exif["DateTaken"]
        try:
            photo_repository.create(
                path=self.image_path,
                name=self.image_path.split("/")[-1],
                date_taken=date_taken,
            )
        except IntegrityError:
            print(f"Photo already exists in database: {self.image_path}")
            photo_repository.session.rollback()

        try:
            exif_repository.create(
                path=self.image_path,
                model=self.exif["Model"],
                make=self.exif["Make"],
                iso=self.exif["ISO"],
                aperture=self.exif["Aperture"],
                shutter_speed=self.exif["ShutterSpeed"],
                exposure_bias=self.exif["ExposureBias"],
                exposure_program=self.exif["ExposureProgram"],
                rotation=self.exif["Rotation"],
                date_taken=date_taken,
            )
        except IntegrityError:
            print(f"Exif already exists in database: {self.image_path}")
            exif_repository.session.rollback()


import_images = ImportImages()
import_images()
