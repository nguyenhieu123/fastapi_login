import models as _models
import schemas as _schemas
import security as _security
import user_crud as _user_crud
from datetime import timedelta
from typing import List
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from database import get_db
from fastapi import FastAPI
from fastapi_profiler.profiler_middleware import PyInstrumentProfilerMiddleware

ACCESS_TOKEN_EXPIRE_MINUTES = 3600

app = FastAPI()
# app.add_middleware(PyInstrumentProfilerMiddleware)

@app.get("", response_model=List[_schemas.UserSchema])
def users(db: Session = Depends(get_db)):
    users = _user_crud.get_all_users(db)
    return list(users)


@app.get("/{email:str}", response_model=_schemas.UserSchema)
def get_user(email: str, db: Session = Depends(get_db)) -> _schemas.UserSchema:
    user = _user_crud.get_user_by_email(db, email)
    if user:
        return user
    else:
        return {'message': 'user not found'}, 404


@app.post("/sign_up", response_model=_schemas.UserSchema)
def sign_up(
        user_data: _schemas.UserCreateSchema, db: Session = Depends(get_db)):
    user = _user_crud.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="email exist",
        )
    new_user = _user_crud.add_user(db, user_data)
    return new_user


@app.post("/login")
def login_for_access_token(form_data: _schemas.Login,
                            db: Session = Depends(get_db)
):
    user_data = _security.authenticate_user(
        db, form_data.email, form_data.password)
    if not user_data:
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            detail="invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expires_date = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _security.create_access_token(
        data={'sub': user_data.email},
        expires_delta=token_expires_date,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get("me", response_model=_schemas.UserSchema)
def get_current_user(
        user_data: _models.UserModel = Depends(_user_crud.get_current_user)):
    return user_data