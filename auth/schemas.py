from pydantic import ConfigDict
from typing import Optional, List
from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, Field
from pydantic.version import VERSION as PYDANTIC_VERSION

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    username: str
    phone: str
    preferences: List[int]

    if PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    username: str
    phone: str
    preferences: List[int]
