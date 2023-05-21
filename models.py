import sqlalchemy

import database as _db


class User(_db.Base):
  __tableame__ = 'users'
  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
  email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
  hashed_password = sqlalchemy.Column(sqlalchemy.String)