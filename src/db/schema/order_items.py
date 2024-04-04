from cuid2 import cuid_wrapper

import sqlalchemy as sa
import sqlalchemy.orm as orm

from ..connection import Base, db_session
from .orders import Orders
from .products import Products

cuid_generator = cuid_wrapper()

class OrderItems(Base):
    __tablename__ = 'order_items'
    id = sa.Column(sa.Text,default=cuid_wrapper(),primary_key = True)
    order_id = sa.Column(sa.Text,sa.ForeignKey('orders.id',ondelete='CASCADE'))
    order = orm.relationship('Orders',back_populates='order_items')
    product_id = sa.Column(sa.Text,sa.ForeignKey('products.id',ondelete='SET NULL'))
    product = orm.relationship('Products',backref='products',lazy='joined')
    quantity = sa.Column(sa.Integer,default=1)
    price_in_cents = sa.Column(sa.Integer,nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        super(OrderItems,self).__init__(*args,**kwargs)

    def create(self):
        db_session.add(self)
        db_session.commit()
        return self