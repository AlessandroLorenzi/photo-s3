import io

from PIL import Image

from photo_s3_bucket.libs.image_lister import ImageLister


class Thumbnailizer:
    def __init__(
        self,
        size,
        image_lister: ImageLister,
        thumbnails_image_lister: ImageLister,
        overwrite: bool = False,
    ):
        self.size = size
        self.image_lister = image_lister
        self.thumbnails_image_lister = thumbnails_image_lister
        self.overwrite = overwrite

    def generate(self, image_path: str):
        if self.thumbnails_image_lister.image_exists(image_path) and not self.overwrite:
            print(f"Thumbnail already exists - skipping {image_path}")
            return

        if not self.image_lister.is_image(image_path):
            print(f"Not an image - skipping {image_path}")
            return

        original_image = self.image_lister.get_object(image_path)

        original_format = original_image["ContentType"].split("/")[1]
        original_image_body = original_image["Body"]

        pillow_image = Image.open(original_image_body)
        if "exif" not in pillow_image.info:
            print(f"No EXIF data - skipping {image_path}")
            return
        exif = pillow_image.info["exif"]
        pillow_image.thumbnail(self.size, Image.ANTIALIAS)

        with io.BytesIO() as output:
            pillow_image.save(
                output,
                format=original_format,
                exif=exif,
                quality=95,
            )

            output.seek(0)
            self.thumbnails_image_lister.put_object(image_path, output)
            print(f"Thumbnail created for {image_path}")
