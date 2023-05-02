#!/bin/env python3

import boto3

print("Setting up default session")

boto3.setup_default_session()
dynamodb_client = boto3.client("dynamodb")

TABLE_NAME = "alorenzi-pictures-votes"

print("Creating table")
response = dynamodb_client.create_table(
    TableName=TABLE_NAME,
    BillingMode="PAY_PER_REQUEST",
    KeySchema=[
        {
            "AttributeName": "photo_name",
            "KeyType": "HASH",
        },
    ],
    AttributeDefinitions=[
        {
            "AttributeName": "photo_name",
            "AttributeType": "S",
        },
    ],
)
assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
dynamodb_client.get_waiter("table_exists").wait(
    TableName=TABLE_NAME,
)
print("Table created")


print("Updating table to add rating attribute")
response = dynamodb_client.update_table(
    TableName=TABLE_NAME,
    AttributeDefinitions=[
        {
            "AttributeName": "rating",
            "AttributeType": "N",
        },
    ],
    GlobalSecondaryIndexUpdates=[
        {
            "Create": {
                "IndexName": "rating-index",
                "KeySchema": [
                    {
                        "AttributeName": "rating",
                        "KeyType": "HASH",
                    },
                ],
                "Projection": {
                    "ProjectionType": "ALL",
                },
            },
        },
    ],
)
assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

print("Table updated")
