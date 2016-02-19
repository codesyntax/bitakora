# S3Boto storage settings for photologue example project.

DEFAULT_FILE_STORAGE = 'bitakora.s3storage.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'bitakora.s3storage.s3utils.StaticS3BotoStorage'
AWS_ACCESS_KEY_ID = '0KNPQDS4E6BFHX9Y23R2'
AWS_SECRET_ACCESS_KEY = '18c7nUoXdEr9S20azYqPqizK+5d9a8uk22CUtNK7'
AWS_STORAGE_BUCKET_NAME = 'media.blogak.eus'
AWS_S3_CUSTOM_DOMAIN= 'media.blogak.eus'
MEDIA_URL = 'http://%s/media/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'http://%s/static/' % AWS_STORAGE_BUCKET_NAME

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
if hasattr(ssl, '_create_unverified_context'):
   ssl._create_default_https_context = ssl._create_unverified_context