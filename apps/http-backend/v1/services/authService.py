from v1.models import User
from fastapi import HTTPException
from v1.db.connectDB import getDB
from v1.utility import response
from v1.utility import HashPassword, GenerateEmailVerifyToken, SendVerificationEmail, log

class Auth:
    @property
    async def collection(self):
        return getDB()["User"]

    async def RegisterUser(self, user: registerUser):
        try:
            existUser = await self.collection.find_one({"email": user.email})
            if existUser is not None:
                if existUser.get("is_verified"):
                    raise HTTPException(
                        status_code=409,
                        details={
                            "message":"User is Already Exist with this Email id",
                            "status":False,
                        }
                    )
                else:
                    hashed_password = HashPassword(user.password)
                    await self.collection.update_one(
                        {"email": user.email},
                        {
                            "$set": {
                                "full_name": user.full_name,
                                "password": hashed_password,
                                "role": user.role,
                                "avatar": user.avatar,
                                "phone": user.phone if user.phone else None,
                            }
                        },
                    )
                    
                    verificationToken = await GenerateEmailVerifyToken(user.email)
                    sendMail = await SendVerificationEmail(
                        email=user.email, name=user.full_name, token=verificationToken
                    )
                    if sendMail:
                        return response(
                            message="Verication link is successfully sended to your email ID"
                        )
                    else:
                        raise HTTPException(
                            status_code=500,
                            details={
                                "status":False,
                                "message":"Something went wrong while sending email, please try again",
                            }
                        )

            hashed_password = HashPassword(user.password)
            new_user = User(
                full_name=user.full_name,
                email=user.email,
                password=hashed_password,
                role=user.role,
                avatar=user.avatar,
                phone=user.phone if user.phone else None,
            )
            await self.collection.insert_one(new_user.dict(by_alias=True, exclude={"id"}))

            verificationToken = await GenerateEmailVerifyToken(user.email)
            sendMail = await SendVerificationEmail(
                email=user.email, name=user.full_name, token=verificationToken
            )
            if sendMail:
                return response(
                    message="Verication link is successfully sended to your email ID"
                )
            else:
                raise HTTPException(
                    status_code=500,
                    details={
                        "status":False,
                        "message":"Something went wrong while sending email, please try again",
                    }
                )
        except HTTPException:
            raise
        except Exception as e:
            log.info(f"this is a issue {str(e)}")
            return HTTPException(
                status_code=500,
                details={
                    "message":"Something went wrong while creating a new account, please try again",
                    "status":False
                }
            )

    async def ResendVerificationLink(self,email: str):
        try:
            existUser = await self.collection.find_one({"email": email})
            if existUser is None:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status": False,
                        "message": "User not found with this email Id",
                        "data": None,
                    },
                )

            if existUser.get("is_verified"):
                raise HTTPException(
                    status_code=500,
                    detail={
                        "status": False,
                        "message": "Account already verified, please login",
                        "data": None,
                    },
                )

            verificationToken = await GenerateEmailVerifyToken(existUser.get("email"))

            sendMail = await SendVerificationEmail(
                email=existUser.get("email"), name=existUser.get("full_name"), token=verificationToken
            )

            if sendMail:
                return response(
                    message="Verication link is successfully sended to your email ID"
                )
            else:
                raise HTTPException(
                status_code=500,
                details={
                        "status":False,
                        "message":"Something went wrong while sending email, please try again",
                    }
                )
        except HTTPException:
            raise
        except Exception as e:
            log.info(f"this is a issue {str(e)}")
            return HTTPException(
                status_code=500,
                details={
                "message":"Something went wrong, please try again",
                "status":False
                }
            )
