import jwt
from typing import Optional
from auth.database import User, get_user_db
from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
    
    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        
        password = user_dict.pop("password")
        user_dict["password_hash"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user
    

    async def get_by_refresh_token(self, refresh_token: str) -> User:
        try:
            payload = jwt.decode(refresh_token, "SECRET", algorithms=["HS256"])
            user_id = payload.get("sub")
            user = await self.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=400, detail="Invalid refresh token")
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=400, detail="Refresh token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
