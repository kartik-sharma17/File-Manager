from v1.models import User
from fastapi import HTTPException
from v1.db.connectDB import getDB
from v1.utility import response
from v1.utils.passwordHashing.passwordHashing import HashPassword
from v1.utils.emailVerifyToken.emailVerifyToken import GenerateEmailVerifyToken
from v1.utils.mailConfig.sendVerificationMail import SendVerificationEmail
from v1.schema.authSchema.registerUser import registerUser


async def RegisterUser(user: registerUser):
    try:
        db = getDB()
        existUser = await db["users"].find_one({"email": user.email})
        if existUser is not None:
            if existUser.get("is_verified"):
                return response(
                    message="User is Already Exist with this Email id",
                    code=500,
                    status=False,
                )
            else:
                hashed_password = HashPassword(user.password)
                await db["users"].update_one(
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
                    return response(
                        status=False,
                        code=500,
                        message="Something went wrong while sending email, please try again",
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
        await db["users"].insert_one(new_user.dict(by_alias=True, exclude={"id"}))

        verificationToken = await GenerateEmailVerifyToken(user.email)
        print("this is a verification token", verificationToken)
        sendMail = await SendVerificationEmail(
            email=user.email, name=user.full_name, token=verificationToken
        )
        if sendMail:
            return response(
                message="Verication link is successfully sended to your email ID"
            )
        else:
            return response(
                status=False,
                code=500,
                message="Something went wrong while sending email, please try again",
            )

    except Exception as e:
        print(f"this is a issue {str(e)}")
        return response(
            status=False,
            code=500,
            message="Something went wrong while creating a new account, please try again",
        )


async def ResendVerificationLink(email: str):
    try:
        db = getDB()
        existUser = await db["users"].find_one({"email": email})
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
            return response(
                status=False,
                code=500,
                message="Something went wrong while sending email, please try again",
            )

    except Exception as e:
        print(f"this is a issue {str(e)}")
        return response(
            status=False,
            code=500,
            message="Something went wrong, please try again",
        )
