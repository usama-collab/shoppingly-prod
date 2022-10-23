import os
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "shopingly-space"
AWS_S3_ENDPOINT_URL = "https://fra1.digitaloceanspaces.com"

# setting catch control parameters upto a 1 day
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400"
}
# i.e https://appname.space-bucket-name.url
AWS_LOCATION = "https://shopingly-space.fra1.digitaloceanspaces.com"
DEFAULT_FILE_STORAGE = "shopingly.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "shopingly.cdn.backends.StaticRootS3Boto3Storage"
