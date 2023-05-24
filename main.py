import sqlalchemy.orm as _orm
from passlib.context import CryptContext
import schemas as _schemas
import services as _services
from fastapi.middleware.cors import CORSMiddleware
from models import User

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from fastapi.responses import ORJSONResponse

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

app = FastAPI()

origins = [
  "http://localhost",
  "http://127.0.0.1",
  "http://localhost:3000",
  "http://localhost:3001",
  "http://localhost:5173",
  "http://127.0.0.1:3000"
  "http://127.0.0.1:3001"
  "http://127.0.0.1:5173"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


@app.post("/api/user")
async def create_user(user: _schemas.UserCreate,
                      db: _orm.Session = Depends(_services.get_db)):
  db_user = await _services.get_user_by_email(user.email, db)
  print(db_user)
  if db_user:
    raise HTTPException(status_code=400, detail="Email already in use")

  user_created = await _services.create_user(user, db)

  return await _services.create_token(user_created)


@app.get('/api/users/me', response_model=_schemas.User)
async def get_user(user: _schemas.User = Depends(_services.get_current_user)):
  return user


@app.post("/api/token", response_model=_schemas.TokenRequest)
async def login_for_access_token(
  form_data: OAuth2PasswordRequestForm = Depends(),
  _db: _orm.Session = Depends(_services.get_db)
):
  user = _db.query(User).filter(User.email == form_data.username).first()

  if not user or not pwd_context.verify(form_data.password, user.hashed_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )

  access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=60))
  return {"access_token": access_token, "token_type": "bearer"}
