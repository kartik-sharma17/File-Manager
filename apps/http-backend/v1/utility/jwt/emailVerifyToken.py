from jose import jwt, JWTError, ExpiredSignatureError
from config import settings
from datetime import datetime, timedelta


async def GenerateEmailVerifyToken(email: str):
    expire = datetime.utcnow() + timedelta(minutes=settings.EMAIL_TOKEN_EXPIRE_MINUTES)
    data = {"sub": email, "exp": expire}
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def VerifyEmailToken(token):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return {"status": True, "data": payload, "message": "Verification Completed"}

    except ExpiredSignatureError:
        return {
            "status": False,
            "data": "",
            "message": "Token Expired, Please try Again",
        }

    except JWTError:
        return {
            "status": False,
            "data": "",
            "message": "Invalid Token Please Try Again",
        }
