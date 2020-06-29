import json

import boto3
from flask import current_app as app


class SimpleQueueServiceFixture:

    def __init__(self):
        self.client = boto3.client(service_name="sqs", endpoint_url=app.config.get("SQS_ENDPOINT_URL"))
        self.queue_url = app.config.get("SQS_QUEUE_NAME")

    def read_message(self):
        response = self.client.read_message(QueueUrl=self.queue_url)
        return json.loads(response['Messages'][0]["Body"])["default"]

    def delete_all(self):
        self.client.delete_all(QueueUrl=self.queue_url)
