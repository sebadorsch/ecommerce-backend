import datetime as _dt

import sqlalchemy
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _db


class User(_db.Base):
  __tablename__ = 'users'
  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
  email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
  hashed_password = sqlalchemy.Column(sqlalchemy.String)

  leads = _orm.relationship("Lead", back_populates="owner")

  def verify_password(self, password: str):
    return _hash.bcrypt.verify(password, self.hashed_password)


class Lead(_db.Base):
  __tablename__ = 'leads'
  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
  owner_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
  first_name = sqlalchemy.Column(sqlalchemy.String, index=True)
  last_name = sqlalchemy.Column(sqlalchemy.String, index=True)
  email = sqlalchemy.Column(sqlalchemy.String, index=True)
  company = sqlalchemy.Column(sqlalchemy.String, index=True, default='')
  note = sqlalchemy.Column(sqlalchemy.String, default='')
  date_created = sqlalchemy.Column(sqlalchemy.DateTime, default=_dt.datetime.utcnow)
  date_last_updated = sqlalchemy.Column(sqlalchemy.DateTime, default=_dt.datetime.utcnow)

  owner = _orm.relationship('User', back_populates='leads')
