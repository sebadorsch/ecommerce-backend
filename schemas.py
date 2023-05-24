import datetime as _dt
import pydantic as _pydentic
from pydantic import BaseModel


class _UserBase(_pydentic.BaseModel):
  email: str


class User(_UserBase):
  id: int

  class Config:
    orm_mode = True


class UserCreate(_UserBase):
  hashed_password: str

  class Config:
    orm_mode = True


class _LeadBase(_pydentic.BaseModel):
  first_name: str
  last_name: str
  email: str
  company: str
  note: str


class LeadCreate(_LeadBase):
  pass


class Lead(_LeadBase):
  id: int
  owner_id: int
  date_created: _dt.datetime
  date_last_updated: _dt.datetime

  class Config:
    orm_model = True


class TokenRequest(_pydentic.BaseModel):
  access_token: str
  token_type: str


class UserInDB(User):
  hashed_password: str


class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  username: str | None = None
