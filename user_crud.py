import os
import models as _models
import schemas as _schemas
import security as _security
from typing import Optional, List
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.params import Depends
from starlette import status
from database import get_db


SECRET_KEY = 'ndndfbmndbmndbfsdbmnfdsdbbdfbdfbfdbdbds'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_by_email(db: Session, email: str) -> Optional[_models.UserModel]:
    return db.query(_models.UserModel).filter(
                                 _models.UserModel.email == email).first()


def get_all_users(db: Session) -> List[_models.UserModel]:
    return db.query(_models.UserModel).filter().all()


def add_user(
        db: Session,
        user_data: _schemas.UserCreateSchema) -> _schemas.UserSchema:
    hashed_password = _security.hash_password(user_data.password)
    db_user = _models.UserModel(
        email=user_data.email,
        user_name=user_data.user_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)) -> _models.UserModel:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid JWT",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credential_exception
        token_data = _schemas.TokenDataSchema(email=email)
    except JWTError:
        raise credential_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credential_exception
    return user