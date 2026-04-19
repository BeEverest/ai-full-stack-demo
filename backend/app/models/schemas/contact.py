from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal


class ContactIn(BaseModel):
    name: str
    email: EmailStr
    company: str = ""
    inquiry_type: Literal["cooperation", "media", "other"] = "other"
    message: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("姓名不能为空")
        if len(v) > 100:
            raise ValueError("姓名不能超过100个字符")
        return v

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("留言内容不能为空")
        if len(v) > 2000:
            raise ValueError("留言内容不能超过2000个字符")
        return v


class ContactOut(BaseModel):
    success: bool
    message: str
