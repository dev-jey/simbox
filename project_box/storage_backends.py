from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    bucket_name = 'simbox-static'
    file_overwrite = False