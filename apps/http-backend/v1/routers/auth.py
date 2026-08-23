from fastapi import APIRouter
from v1.schema import registerUser
from v1.services import Auth

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(user: registerUser):
    return await Auth.RegisterUser(user)

@router.get("/verify-email/{token}")
async def verifyEmail(token):
    return await VerifyEmailTokenService(token)


@router.post("/login")
async def login(cred: LoginInputs):
    return await Login(cred)

@router.post("/resend-verification")
async def resendVerificationLink(email: str):
    return await Auth.ResendVerificationLink(email)
