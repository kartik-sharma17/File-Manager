import uuid
from bson import ObjectId
from datetime import datetime, timezone
from fastapi import HTTPException
from v1.db.connectDB import getDB
from v1.schema import UploadRequestSchema, UploadRequestResponseSchema
from v1.utility import (
    log,
    GeneratePresignedUploadUrl,
    GeneratePresignedDownloadUrl,
    VerifyObjectExists,
    response,
)
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

            data = UploadRequestResponseSchema(
                document_id=str(result.inserted_id),
                upload_url=upload_url,
                r2_key=r2_key,
                expires_in=900,
            )

            return response(
                message="Upload URL generated successfully",
                data=data.dict(),
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

    async def ConfirmUpload(self, user: dict, document_id: str):
        try:
            owner_id = str(user["_id"])

            document = await self.collection.find_one({"_id": ObjectId(document_id)})

            if not document:
                raise HTTPException(
                    status_code=404,
                    detail={"status": False, "message": "Document not found"},
                )

            if document["owner_id"] != owner_id:
                raise HTTPException(
                    status_code=403,
                    detail={"status": False, "message": "You do not have access to this document"},
                )

            actual_size = await VerifyObjectExists(document["url"])

            if actual_size is None:
                await self.collection.update_one(
                    {"_id": ObjectId(document_id)},
                    {"$set": {"status": "failed", "updated_at": datetime.now(timezone.utc)}},
                )
                raise HTTPException(
                    status_code=400,
                    detail={
                        "status": False,
                        "message": "Upload could not be verified — file not found in storage",
                    },
                )

            expected_size = document.get("size")

            if expected_size is not None and actual_size != expected_size:
                await self.collection.update_one(
                    {"_id": ObjectId(document_id)},
                    {"$set": {"status": "failed", "updated_at": datetime.now(timezone.utc)}},
                )
                raise HTTPException(
                    status_code=400,
                    detail={
                        "status": False,
                        "message": f"Upload incomplete — expected {expected_size} bytes, got {actual_size} bytes",
                    },
                )

            await self.collection.update_one(
                {"_id": ObjectId(document_id)},
                {
                    "$set": {
                        "status": "completed",
                        "size": actual_size,
                        "updated_at": datetime.now(timezone.utc),
                    }
                },
            )

            return response(
                message="Upload confirmed",
                data={"document_id": document_id, "size": actual_size},
            )

        except HTTPException:
            raise
        except Exception as e:
            log.info(f"this is a issue {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={"status": False, "message": "Something went wrong while confirming upload"},
            )

    async def GetDownloadUrl(self, user: dict, document_id: str):
        try:
            document = await self.collection.find_one({"_id": ObjectId(document_id)})

            if not document:
                raise HTTPException(
                    status_code=404,
                    detail={"status": False, "message": "Document not found"},
                )

            if not document.get("is_public"):
                owner_id = str(user["_id"]) if user else None
                if owner_id != document["owner_id"]:
                    raise HTTPException(
                        status_code=403,
                        detail={"status": False, "message": "You do not have access to this document"},
                    )

            download_url = await GeneratePresignedDownloadUrl(key=document["url"])

            if not download_url:
                raise HTTPException(
                    status_code=500,
                    detail={
                        "status": False,
                        "message": "Something went wrong while generating download URL, please try again",
                    },
                )

            return response(
                message="Download URL generated successfully",
                data={
                    "file_name": document["file_name"],
                    "download_url": download_url,
                    "expires_in": 900,
                },
            )

        except HTTPException:
            raise
        except Exception as e:
            log.info(f"this is a issue {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={"status": False, "message": "Something went wrong while generating download URL"},
            )


document_service = DocumentService()