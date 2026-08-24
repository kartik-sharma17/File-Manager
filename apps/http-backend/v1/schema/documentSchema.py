from pydantic import BaseModel, Field, field_validator
from typing import Optional


MAX_FILE_SIZE = 100 * 1024 * 1024


class UploadRequestSchema(BaseModel):
    file_name: str = Field(..., min_length=1, max_length=255)
    mime_type: str = Field(..., min_length=1)
    size: int = Field(..., gt=0, le=MAX_FILE_SIZE)
    is_public: bool = False

    @field_validator("file_name")
    @classmethod
    def sanitize_file_name(cls, v: str) -> str:
        if "/" in v or "\\" in v or ".." in v:
            raise ValueError("Invalid file name")
        return v


class UploadRequestResponseSchema(BaseModel):
    document_id: str
    upload_url: str
    r2_key: str
    expires_in: int = 900


class ConfirmUploadSchema(BaseModel):
    document_id: str


class GetDocumentResponseSchema(BaseModel):
    id: str
    file_name: str
    mime_type: str
    size: int
    is_public: bool
    status: str
    url: Optional[str] = None     
    share_token: Optional[str] = None
    created_at: str