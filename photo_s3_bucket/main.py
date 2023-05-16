#!/usr/bin/env python3

from flask import Flask, send_from_directory

from photo_s3_bucket.container import Container
from photo_s3_bucket.pages.details import details
from photo_s3_bucket.pages.gallery_segment import gallery_segment
from photo_s3_bucket.pages.navigation import navigation
from photo_s3_bucket.pages.tags import add_tag, delete_tag, get_tags
from photo_s3_bucket.pages.vote import get_vote, update_vote
from photo_s3_bucket.pages.search import search

if __name__ == "__main__":
    container = Container()
    container.wire(
        modules=[
            "photo_s3_bucket.pages.navigation",
            "photo_s3_bucket.pages.details",
            "photo_s3_bucket.pages.vote",
            "photo_s3_bucket.pages.tags",
            "photo_s3_bucket.pages.search",
            "photo_s3_bucket.pages.gallery_segment",
        ]
    )

    app = Flask(__name__)
    app.container = container

    app.add_url_rule("/", "index", navigation)
    app.add_url_rule("/gallery_segment", "gallery_segment", gallery_segment)

    app.add_url_rule("/details", "details", details)
    app.add_url_rule("/vote", "get_vote", get_vote)
    app.add_url_rule("/vote", "update_vote", update_vote, methods=["PUT"])

    TAGS_ROUTE = "/tags"
    app.add_url_rule(TAGS_ROUTE, "get_tags", get_tags)
    app.add_url_rule(TAGS_ROUTE, "delete_tag", delete_tag, methods=["DELETE"])
    app.add_url_rule(TAGS_ROUTE, "add_tag", add_tag, methods=["POST"])

    app.add_url_rule("/search", "search", search)

    @app.route('/photos/<path:filename>')
    def serve_photos(filename):
        root_dir = '../test_pictures'
        return send_from_directory(root_dir, filename)

    app.run(host="0.0.0.0", debug=True)
