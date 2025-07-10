from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from enum import Enum
from typing import Optional

class UserBaseSchema(BaseModel):
    email: EmailStr

class UserCreateSchema(UserBaseSchema):
    email: EmailStr = Field(..., max_length=100)

class UserUpdateSchema(UserBaseSchema):
    email: EmailStr | None = None


class UserSchema(UserBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)



