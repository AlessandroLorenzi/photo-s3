class TagsService:
    def __init__(self, dynamodb_client, table_name):
        self.dynamodb_client = dynamodb_client
        self.table_name = table_name

    def set(self, photo_name: str, tags: list):
        self.dynamodb_client.put_item(
            TableName=self.table_name,
            Item={
                "photo_name": {
                    "S": photo_name,
                },
                "tags": {
                    "SS": tags,
                },
            },
        )

    def get_tags(self, photo_name):
        resp = self.dynamodb_client.get_item(
            TableName=self.table_name,
            Key={
                "photo_name": {
                    "S": photo_name,
                },
            },
        )
        if "Item" not in resp:
            return []
        return resp["Item"]["tags"]["SS"]

    def get_photos(self, tag):
        resp = self.dynamodb_client.scan(
            TableName=self.table_name,
            FilterExpression="contains(tags, :tag)",
            ExpressionAttributeValues={
                ":tag": {
                    "S": tag,
                },
            },
        )
        return [item["photo_name"]["S"] for item in resp["Items"]]

    def add_tag(self, photo_name, tag):
        tags = self.get_tags(photo_name)
        tags.append(tag)
        self.set(photo_name, tags)

    def drop_tag(self, photo_name, tag):
        tags = self.get_tags(photo_name)
        tags.remove(tag)
        if len(tags) == 0:
            self.dynamodb_client.delete_item(
                TableName=self.table_name,
                Key={
                    "photo_name": {
                        "S": photo_name,
                    },
                },
            )
            return
        self.set(photo_name, tags)
