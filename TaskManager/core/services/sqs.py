from datetime import datetime
from os import environ

import boto3


class SQSService:

    def __init__(self):
        self.key = environ["AWSAccessKeyId"]
        self.secret = environ["AWSSecretKey"]
        self.region = environ["AWSRegion"]

        self.url = environ["AWSSQSurl"]

        self.client = boto3.client(
            'sqs',
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
            region_name=self.region,
        )

    def send_message(self, email):
        resp = self.client.send_message(
            QueueUrl=self.url,
            MessageBody=f'Sending mail to {email}',
            DelaySeconds=0,
            MessageAttributes={
                'Email': {
                    'DataType': 'String',
                    'StringValue': email
                },
            },
            MessageDeduplicationId=str(datetime.utcnow().timestamp()),
            MessageGroupId=str(datetime.utcnow().timestamp()),
        )
