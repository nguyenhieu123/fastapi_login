from datetime import timedelta, datetime
from typing import Union, Optional

from fastapi.security import OAuth2PasswordBearer
import passlib.hash as _hash
from sqlalchemy.orm import Session
import jose as _jose
import user_crud as _user_crud
import models as _models

SECRET_KEY = 'ndndfbmndbmndbfsdbmnfdsdbbdfbdfbfdbdbds'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(plain_password: str) -> str:
    return _hash.sha256_crypt.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _hash.sha256_crypt.verify(plain_password, hashed_password)


def authenticate_user(
                        db: Session,
                        email: str, password: str) -> Union[
                                                            bool,
                                                            _models.UserModel]:
    user: _models.UserModel = _user_crud.get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expires})
    encoded_jwt = _jose.jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt