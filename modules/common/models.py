from modules.common.db_init import db
from sqlalchemy import Column, Integer, TIMESTAMP, text
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.now(), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.now(), server_default=text('CURRENT_TIMESTAMP'), onupdate=datetime.now(), nullable=False)

    @classmethod
    def new(cls, **kwargs):
        new_obj = cls(**kwargs)
        db.session.add(new_obj)
        return new_obj
