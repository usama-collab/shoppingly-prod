import os
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = "https://fra1.digitaloceanspaces.com"

# setting catch control parameters upto a 1 day
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400"
}
# i.e https://space-bucket-name.appname.url
AWS_LOCATION = "https://{AWS_STORAGE_BUCKET_NAME}.fra1.ondigitalocean.app"

DEFAULT_FILE_STORAGE = "shopingly.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "shopingly.cdn.backends.StaticRootS3Boto3Storage"
