from os import environ

import boto3


class SESService:
    def __init__(self):
        self.key = environ["AWSAccessKeyId"]
        self.secret = environ["AWSSecretKey"]
        self.region = environ["AWSRegion"]
        self.client = boto3.client(
            'ses',
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
            region_name=self.region,
        )

    def send_email(self, email):
        response = self.client.send_email(
            Source='jordan.v.dimov@gmail.com',
            Destination={
                'ToAddresses': [
                    email,
                ],
            },
            Message={
                'Subject': {
                    'Data': 'The Task Management System Welcomes You!',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': 'Hello, you are registered in the Task Management System',
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': 'Hello, you are registered in the Task Management System',
                        'Charset': 'UTF-8'
                    }
                }
            },
        )
