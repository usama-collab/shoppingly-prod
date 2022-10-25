import os
from decouple import config

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = "https://fra1.digitaloceanspaces.com"

# setting catch control parameters upto a 1 day
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400"
}
# i.e https://space-bucket-name.spacenameurl
AWS_LOCATION = f"https://{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com"

DEFAULT_FILE_STORAGE = "shoppingly.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "shoppingly.cdn.backends.StaticRootS3Boto3Storage"
