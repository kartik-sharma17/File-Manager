from fastapi import APIRouter
from v1.schema import registerUser, LoginSchema
from v1.services import Auth

authrouter = APIRouter(prefix="/auth", tags=["auth"])


@authrouter.post("/register")
async def register(user: registerUser):
    return await Auth.RegisterUser(user)

@authrouter.get("/verify-email/{token}")
async def verifyEmail(token):
    return await Auth.VerifyAccount(token)


@authrouter.post("/login")
async def login(cred: LoginSchema):
    return await Auth.Login(cred)

@authrouter.post("/resend-verification")
async def resendVerificationLink(email: str):
    return await Auth.ResendVerificationLink(email)
