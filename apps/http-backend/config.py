from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGO_URL: str = os.getenv("MONGO_URL")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    ACCESS_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_EXPIRE_MINUTES"))
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")

    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS")
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")

    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY")

settings = Settings()
