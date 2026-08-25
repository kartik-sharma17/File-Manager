from fastapi import APIRouter, Depends
from v1.schema import UploadRequestSchema
from v1.services import document_service
from v1.dependencies import verifyUserDependency

documentRouter = APIRouter(prefix="/document", tags=["document"])

@documentRouter.post("/create")
async def register(documentData: UploadRequestSchema, user = Depends(verifyUserDependency)):
    return await document_service.UploadDocument(user,documentData)

# @documentRouter.put("/update/{id}")
# async def verifyEmail(token):
#     return await Auth.VerifyAccount(token)

# @documentRouter.delete("/delete/{id}")
# async def login(cred: LoginSchema):
#     return await Auth.Login(cred)

# @documentRouter.get("/get")
# async def resendVerificationLink(email: str):
#     return await Auth.ResendVerificationLink(email)
