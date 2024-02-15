from cuid2 import cuid_wrapper

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

from ..connection import Base, db_session

cuid_generator = cuid_wrapper()

class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Text,default=cuid_wrapper(),primary_key = True)
    name = sa.Column(sa.Text)
    email = sa.Column(sa.Text,nullable=False,unique=True)
    phone = sa.Column(sa.Text)
    role = sa.Column(ENUM('manager','customer',name='user_role'))
    created_at = sa.Column(sa.DateTime(timezone=True),server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True),server_default=sa.func.now(),onupdate=sa.func.now())

    def __init__(self, name: str, phone: str, *args, **kwargs) -> None:
        super(User,self).__init__(*args,**kwargs)
        self.name = name
        self.phone = phone

    def create(self):
        db_session.add(self)
        db_session.commit()
        return self