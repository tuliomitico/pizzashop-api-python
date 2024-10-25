from sqlalchemy import func
from flask_jwt_extended import get_jwt
from flask_smorest import Blueprint
from marshmallow import fields

from ..authentication import jwt_required_with_doc
from ...schemas import ma
from ...db.schema import Orders, User, OrderItems, Products

class PopularProductsSchema(ma.Schema):
    product = fields.String()
    amount = fields.Integer()

popular_products_blp = Blueprint("popular_products", "popular_products", url_prefix="/metrics/popular-products", description="Operations on popular products")

@popular_products_blp.route("",methods=['GET'])
# @popular_products_blp.arguments(OrdersBodySchema,location='query')
@jwt_required_with_doc(locations=['cookies'])
def index():
  restaurant = get_jwt()
  restaurant_id = restaurant['restaurant_id']

  if not restaurant_id:
    return {"error":"User is not a restaurant manager"}, 401
  
  raw_popular_products = OrderItems.query.with_entities(
      Products.name.label('product'),
      func.count(OrderItems.order_id).label('amount')
  ).join(Orders,Orders.id == OrderItems.order_id).join(Products,Products.id == OrderItems.product_id).filter(Orders.restaurant_id==restaurant_id).group_by(
      Products.name
  )
  
  popular_products = PopularProductsSchema().dump(raw_popular_products.limit(5),many=True)

  return popular_products, 200
