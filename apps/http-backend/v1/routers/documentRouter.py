from fastapi import APIRouter, Depends
from v1.schema import UploadRequestSchema
from v1.services import document_service
from v1.dependencies import verifyUserDependency

documentRouter = APIRouter(prefix="/document", tags=["document"])


@documentRouter.post("/create")
async def createDocument(documentData: UploadRequestSchema, user=Depends(verifyUserDependency)):
    return await document_service.UploadDocument(user, documentData)


@documentRouter.post("/confirm/{document_id}")
async def confirmUpload(document_id: str, user=Depends(verifyUserDependency)):
    return await document_service.ConfirmUpload(user, document_id)


@documentRouter.get("/download/{document_id}")
async def getDownloadUrl(document_id: str, user=Depends(verifyUserDependency)):
    return await document_service.GetDownloadUrl(user, document_id)