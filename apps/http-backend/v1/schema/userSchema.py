from pydantic import BaseModel,EmailStr
from typing import Optional

class registerUser(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str
    avatar: Optional[str] = None
    phone: Optional[str] = None
