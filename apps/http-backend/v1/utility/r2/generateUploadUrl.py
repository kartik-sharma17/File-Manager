import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from config import settings
from v1.utility import log


def get_storage_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.B2_ENDPOINT_URL,
        aws_access_key_id=settings.B2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.B2_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
    )


async def GeneratePresignedUploadUrl(key: str, content_type: str, expires_in: int = 900):
    try:
        client = get_storage_client()

        upload_url = client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": settings.B2_BUCKET_NAME,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )

        return upload_url

    except ClientError as e:
        log.info(f"B2 presigned URL generation failed: {str(e)}")
        return None
    except Exception as e:
        log.info(f"this is a issue {str(e)}")
        return None