#!/usr/bin/env python3

from flask import Flask

from photo_s3_bucket.container import Container
from photo_s3_bucket.pages.details import details
from photo_s3_bucket.pages.navigation import navigation
from photo_s3_bucket.pages.vote import get_vote, update_vote

if __name__ == "__main__":
    container = Container()
    container.wire(
        modules=[
            "photo_s3_bucket.pages.navigation",
            "photo_s3_bucket.pages.details",
            "photo_s3_bucket.pages.vote",
        ]
    )

    app = Flask(__name__)
    app.container = container

    app.add_url_rule("/", "index", navigation)
    app.add_url_rule("/details", "details", details)
    app.add_url_rule("/vote", "get_vote", get_vote)
    app.add_url_rule("/vote", "update_vote", update_vote, methods=["PUT"])

    app.run(host="0.0.0.0", debug=True)
