from flask_jwt_extended import get_jwt
from flask_smorest import Blueprint
from marshmallow import fields

from ..authentication import jwt_required_with_doc
from ...schemas import ma
from ...db.schema import Orders, OrderItems, User, Products

class OrdersDetailParamsSchema(ma.Schema):
  order_id = fields.String()

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model=User
class ProductsSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model=Products
    include_relationships=True
    include_fk=True
    load_instance = True
  
class OrderItemsSchema(ma.SQLAlchemyAutoSchema):
  priceInCents=fields.Number(attribute='price_in_cents')
  class Meta:
    model=OrderItems
    include_relationships=True
    # include_fk=True
    load_instance = True
    exclude=['order','price_in_cents']

  product = fields.Nested(ProductsSchema)



class OrderSchema(ma.SQLAlchemyAutoSchema):
  totalInCents=fields.Number(attribute='total_in_cents')
  customer = fields.Nested(UserSchema)
  orderItems = fields.Nested(OrderItemsSchema,many=True,attribute='order_items')
  createdAt = fields.String(attribute='created_at')

  class Meta:
    model=Orders
    strict=True
    include_relationships=True
    include_fk=True
    exclude=['total_in_cents','created_at','order_items']

  
  

order_blp = Blueprint("order_details", "orders", url_prefix="/orders", description="Operations on order details")

@order_blp.route("/<order_id>",methods=['GET'])
# @order_blp.arguments(OrdersDetailParamsSchema,location='path')
@jwt_required_with_doc(locations=['cookies'])
def index(order_id):
  restaurant = get_jwt()
  restaurant_id = restaurant['restaurant_id']

  if not restaurant_id:
    return {"error":"User is not a restaurant manager"}, 401
  
  raw_order = Orders.query.filter_by(id = order_id).filter_by(restaurant_id = restaurant_id) 

  order = OrderSchema().dump(raw_order.first())

  return order, 200
