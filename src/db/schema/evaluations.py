from cuid2 import cuid_wrapper

import sqlalchemy as sa
import sqlalchemy.orm as orm

from ..connection import Base, db_session
from .users import User
from .restaurants import Restaurants

cuid_generator = cuid_wrapper()

class Evaluations(Base):
    __tablename__ = 'evaluations'
    id = sa.Column(sa.Text,default=cuid_wrapper(),primary_key = True)
    customer_id = sa.Column(sa.Text,sa.ForeignKey('users.id'))
    customer = orm.relationship('User')
    restaurant_id = sa.Column(sa.Text,sa.ForeignKey('restaurants.id'))
    restaurant = orm.relationship('Restaurants')
    comment = sa.Column(sa.Text)
    rate = sa.Column(sa.Integer,nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True),server_default=sa.func.now())

    def __init__(self, *args, **kwargs) -> None:
        super(Evaluations,self).__init__(*args,**kwargs)

    def create(self):
        db_session.add(self)
        db_session.commit()
        return self