import os

import boto3
from werkzeug.utils import secure_filename
import uuid


class BotoCRUD:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = 'jusense-landslide'

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
        self.s3.put_object(Body=data, Bucket=self.bucket, Key=filename, ContentType=content_type)


if __name__ == '__main__':
    obj = BotoCRUD()
    obj.list_s3_buckets()
