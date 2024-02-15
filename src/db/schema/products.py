from cuid2 import cuid_wrapper

import sqlalchemy as sa
import sqlalchemy.orm as orm

from ..connection import Base, db_session
from .restaurants import Restaurants

cuid_generator = cuid_wrapper()

class Products(Base):
    __tablename__ = 'products'
    id = sa.Column(sa.Text,default=cuid_wrapper(),primary_key = True)
    name = sa.Column(sa.Text,nullable=False)
    description = sa.Column(sa.Text)
    price_in_cents = sa.Column(sa.Integer,nullable=False)
    restaurant_id = sa.Column(sa.Text,sa.ForeignKey('restaurants.id'))
    restaurant = orm.relationship('Restaurants')
    created_at = sa.Column(sa.DateTime(timezone=True),server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True),server_default=sa.func.now(),onupdate=sa.func.now())

    def __init__(self, *args, **kwargs) -> None:
        super(Products,self).__init__(*args,**kwargs)
   

    def create(self):
        db_session.add(self)
        db_session.commit()
        return self