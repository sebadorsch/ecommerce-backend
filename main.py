import fastapi as _fastapi
import sqlalchemy.orm as _orm
import fastapi.security as _security
import schemas as _schemas
import services as _services
from fastapi.middleware.cors import CORSMiddleware

app = _fastapi.FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/user")
async def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
  db_user = await _services.get_user_by_email(user.email, db)
  if db_user:
    raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

  user_created = await _services.create_user(user, db)

  return await _services.create_token(user_created)


@app.post('/api/token')
async def generate_token(
  form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
  db: _orm.Session = _fastapi.Depends(_services.get_db)):

  user = await _services.authenticate_user(form_data.username, form_data.password, db)

  if not user:
    raise _fastapi.HTTPException(status_code=401, detail='Invalid Credentials')

  return await _services.create_token(user)


@app.get('/api/users/me', response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
  return user
