import boto3
import json
from kitchensink.conf import settings


def get_bucket(mode="preview"):
    bucket_name = (
        settings.AWS_S3_PREVIEW_BUCKET
        if mode == "preview" else
        settings.AWS_S3_PRODUCTION_BUCKET
    )

    session = boto3.session.Session(
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    s3 = session.resource('s3')

    return s3.Bucket(bucket_name)


class Defaults(object):
    OUTPUT_ROOT = settings.PUBLISH_PATH
    MAX_AGE = 500


defaults = Defaults


def publish_to_aws(
    filepath,
    data,
    mode="preview",
    contentType="application/json",
    max_age=defaults.MAX_AGE
):
    key = "{}{}".format(
        defaults.OUTPUT_ROOT,
        filepath
    )

    if key[0] == '/':
        key = key[1:]

    acl = 'bucket-owner-full-control' if mode == 'preview' else 'public-read'

    bucket = get_bucket(mode)
    bucket.put_object(
        Key=key,
        ACL=acl,
        Body=json.dumps(data),
        CacheControl="max-age={}".format(
            max_age if max_age is not None else defaults.MAX_AGE
        ),
        ContentType=contentType
    )
