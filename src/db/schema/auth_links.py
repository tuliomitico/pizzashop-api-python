from cuid2 import cuid_wrapper

import sqlalchemy as sa
import sqlalchemy.orm as orm

from ..connection import Base, db_session
from . import User

cuid_generator = cuid_wrapper()

class AuthLinks(Base):
    __tablename__ = 'auth_links'
    id = sa.Column(sa.Text,default=cuid_wrapper(),primary_key = True)
    code = sa.Column(sa.Text,nullable=False,unique=True)
    user = orm.relationship('User')
    user_id = sa.Column(sa.Text,sa.ForeignKey('users.id',ondelete='CASCADE'))
    created_at = sa.Column(sa.DateTime(timezone=True),server_default=sa.func.now())

    def __init__(self, *args, **kwargs) -> None:
        super(AuthLinks,self).__init__(*args,**kwargs)

    def create(self):
        db_session.add(self)
        db_session.commit()
        return self