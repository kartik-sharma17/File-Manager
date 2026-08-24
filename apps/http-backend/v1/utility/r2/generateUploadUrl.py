import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from config import settings
from v1.utility import log


def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


async def GeneratePresignedUploadUrl(key: str, content_type: str, expires_in: int = 900):
    try:
        client = get_r2_client()

        upload_url = client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": settings.R2_BUCKET_NAME,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )

        return upload_url

    except ClientError as e:
        log.info(f"R2 presigned URL generation failed: {str(e)}")
        return None
    except Exception as e:
        log.info(f"this is a issue {str(e)}")
        return None