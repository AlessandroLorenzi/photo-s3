from photo_s3_bucket.pages.gallery_segment import gallery_segment


class TestGallerySegment:
    def test_gallery_segment(self):
        assert len(gallery_segment()) == 10
