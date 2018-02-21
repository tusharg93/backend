from odyssey import app
import boto3

class UploadToS3Helper:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.base_uri = 'https://s3.us-east-2.amazonaws.com'

    def upload(self, file_name, content, content_type):
        app.logger.info("upload: bucket_name {}".format(self.bucket_name))
        s3 = boto3.resource('s3')
        s3.Bucket(self.bucket_name).put_object(
            Key=file_name,
            Body=content,
            ContentType=content_type
        )
        return '{}/{}/{}'.format(self.base_uri, self.bucket_name, file_name)