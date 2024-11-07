import jwt
import asyncio
from models import User
from datetime import datetime
from pydantic import BaseModel
from auth.database import User
from sqlalchemy.orm import Session
from auth.auth import auth_backend, JWTStrategy
from sqlalchemy import create_engine
from fastapi_users import FastAPIUsers
from auth.schemas import UserCreate, UserRead
from fastapi import Depends, FastAPI, HTTPException
from auth.manager import get_user_manager, UserManager


app = FastAPI()

def generate_refresh_token(user_id: str, secret: str, lifetime_seconds: int) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=lifetime_seconds),
    }
    return jwt.encode(payload, secret, algorithm="HS256")

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

fastapi_users = FastAPIUsers[User, int] (
    get_user_manager,
    [auth_backend]
)

@app.get('/')
def message():
    return {'message': "Hello, world!"}

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.delete("/delete_users")
def delete_user(id1: int):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    engine = create_engine(f"postgresql+asyncpg://postgres:345456zahar@"
                            f"localhost:5432/hakaton?async_fallback=True")
    session = Session(bind=engine)
    data = session.query(User).filter(User.id == id1).delete()
    if not data:
        return {"message": "User does not exist"}
    else:
        session.commit()
        return {"message": "User deleted"}


@app.post("/auth/jwt/refresh")
async def refresh_token(
    refresh_token: str,
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        user = await user_manager.get_by_refresh_token(refresh_token)
        new_access_token = await user_manager.generate_access_token(user)
        return {"access_token": new_access_token, "token_type": "bearer"}
    except Exception as e:
        return {"detail": str(e)}
""" async def refresh_token(
    refresh_token: generate_refresh_token,
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        payload = jwt.decode(refresh_token, "SECRET", algorithms=["HS256"])
        user_id = payload.get("sub")
        user = await user_manager.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

        new_access_token = await user_manager.generate_access_token(user)
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Refresh token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid refresh token") """
