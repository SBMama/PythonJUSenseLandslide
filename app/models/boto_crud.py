import json
import os

import boto3
from werkzeug.utils import secure_filename
import uuid


class BotoCRUD:
    def __init__(self):
        self.s3 = boto3.client('s3',
                               aws_access_key_id='AKIATBRTRCP7ZE4ZJB6Q',
                               aws_secret_access_key='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',
                               region_name='us-east-1')
        self.bucket = 'jusense-landslide'
        self.session = boto3.Session(
                aws_access_key_id='AKIATBRTRCP7ZE4ZJB6Q',
                aws_secret_access_key='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')

    def list_s3_buckets(self):
        response = self.s3.list_buckets()
        print(response)

    def save_image_file(self, file, request):
        id = str(uuid.uuid4())
        content_type = request.mimetype
        filename = id+"."+str(file.filename).split(".")[-1]
        self.s3.put_object(Body=file, Bucket=self.bucket, Key=filename, ContentType=content_type)
        return filename

    def save_metadata_file(self, data, request, filename):
        content_type = request.mimetype
        self.s3.put_object(Body=json.dumps(data), Bucket=self.bucket, Key=filename, ContentType=content_type)

    def fetch_metadata(self):
        metadata = []
        images = []
        s3 = self.session.resource('s3')
        my_bucket = s3.Bucket(self.bucket)
        for my_bucket_object in my_bucket.objects.all():
            if my_bucket_object.key.endswith(".json"):
                metadata.append(json.loads(my_bucket_object.get()['Body'].read()))
            else:
                images.append(my_bucket_object.get()['Body'].read())
        return metadata, images


if __name__ == '__main__':
    obj = BotoCRUD()
    obj.fetch_metadata()
