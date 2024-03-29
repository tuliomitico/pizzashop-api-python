from flask_jwt_extended import get_jwt
from flask_smorest import Blueprint
from marshmallow import fields

from ..authentication import jwt_required_with_doc
from ...schemas import ma
from ...db.schema import Orders, User

class OrdersBodySchema(ma.Schema):
  pageIndex = fields.Number()
  orderId = fields.String()
  customerName = fields.String()
  status = fields.String()

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model=User  
class OrderSchema(ma.SQLAlchemyAutoSchema):
  orderId = fields.String(attribute='id')
  customerName = fields.String(attribute='customer.name')
  total=fields.Number(attribute='total_in_cents')
  customer = fields.Nested(UserSchema)
  createdAt = fields.String(attribute='created_at')

  class Meta:
    model=Orders
    strict=True
    include_relationships=True
    include_fk=True
    exclude=['id','customer','total_in_cents','created_at']
  

blp = Blueprint("orders", "orders", url_prefix="/orders", description="Operations on orders")

@blp.route("",methods=['GET'])
@blp.arguments(OrdersBodySchema,location='query')
@jwt_required_with_doc(locations=['cookies'])
def index(query):
  restaurant = get_jwt()
  restaurant_id = restaurant['restaurant_id']

  if not restaurant_id:
    return {"error":"User is not a restaurant manager"}, 401
  
  raw_orders = Orders.query.filter_by(restaurant_id=restaurant_id).order_by(Orders.created_at.desc()).limit(10).offset(query['pageIndex'])

  orders = OrderSchema().dump(raw_orders,many=True)

  result = {
    "orders": orders,
    "meta": {
      "pageIndex": query['pageIndex'],
      "totalCount": raw_orders.count()
    }
  }

  return result, 200
