import uuid
from datetime import datetime, timezone
from fastapi import HTTPException
from v1.db.connectDB import getDB
from v1.schema import UploadRequestSchema, UploadRequestResponseSchema
from v1.utility import log, GeneratePresignedUploadUrl
from v1.models import Document


class DocumentService:
    @property
    def collection(self):
        return getDB()["Document"]

    async def UploadDocument(self, user: dict, documentData: UploadRequestSchema):
        try:
            owner_id = str(user["_id"])

            file_extension = ""
            if "." in documentData.file_name:
                file_extension = documentData.file_name.rsplit(".", 1)[-1]

            r2_key = (
                f"{owner_id}/{uuid.uuid4()}.{file_extension}"
                if file_extension
                else f"{owner_id}/{uuid.uuid4()}"
            )

            upload_url = await GeneratePresignedUploadUrl(
                key=r2_key,
                content_type=documentData.mime_type,
                expires_in=900,
            )

            if not upload_url:
                raise HTTPException(
                    status_code=500,
                    detail={
                        "status": False,
                        "message": "Something went wrong while generating upload URL, please try again",
                    },
                )

            new_document = Document(
                owner_id=owner_id,
                file_name=documentData.file_name,
                url=r2_key,
                mime_type=documentData.mime_type,
                size=documentData.size,
                is_public=documentData.is_public,
                share_token=None,
                status="uploading",
                checksum=None,
                created_at=datetime.now(timezone.utc),
                updated_at=None,
            )

            result = await self.collection.insert_one(
                new_document.dict(by_alias=True, exclude={"id"})
            )

            return UploadRequestResponseSchema(
                document_id=str(result.inserted_id),
                upload_url=upload_url,
                r2_key=r2_key,
                expires_in=900,
            )

        except HTTPException:
            raise
        except Exception as e:
            log.info(f"this is a issue {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "status": False,
                    "message": "Something went wrong while uploading document, please try again",
                },
            )


document_service = DocumentService()