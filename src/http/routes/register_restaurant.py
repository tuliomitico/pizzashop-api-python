import typing as t


from cuid2 import cuid_wrapper
from flask import request
from flask_smorest import Blueprint
from marshmallow import fields


from ...schemas import ma
from ...db.schema import Restaurants, User

cuid_generator = cuid_wrapper()

class BodySchema(ma.Schema):
  email = fields.Email()
  restaurantName = fields.String()
  managerName = fields.String()
  phone = fields.String()



restaurant_blp = Blueprint("restaurant", "restaurant", url_prefix="/restaurants", description="Operations on restaurant")

@restaurant_blp.route("",methods=['POST'])
@restaurant_blp.arguments(BodySchema,location='json')
def index(body):
  manager = User(
    name=body['managerName'],
    phone=body['phone'],
    role='manager',
    email=body['email']
  ).create()

  Restaurants(
    manager_id=manager.id,
    name=body['restaurantName'],
  ).create()

  return '', 200
