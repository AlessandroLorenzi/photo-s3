#!/usr/bin/env python3

from flask import Flask
from photo_s3_bucket.pages.navigation import navigation
from photo_s3_bucket.pages.details import details
from photo_s3_bucket.pages.vote import vote

app = Flask(__name__)

@app.route("/")
def get_navigation():
    return navigation()

@app.route("/details")
def get_details():
    return details()

@app.route("/vote", methods=['PUT'])
def put_vote():
    return vote()

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8080,
    )


