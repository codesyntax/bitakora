from storages.backends.s3boto import S3BotoStorage
from django.conf import settings

StaticS3BotoStorage = lambda: S3BotoStorage(location='static')
MediaS3BotoStorage = lambda: S3BotoStorage(location='media')
