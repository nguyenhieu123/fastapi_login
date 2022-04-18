from sqlalchemy import Column, Integer, String

from database import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)