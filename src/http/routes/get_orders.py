from flask_smorest import Blueprint
from marshmallow import fields

from ...schemas import ma
from ...db.schema import User

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User

blp = Blueprint("orders", "orders", url_prefix="/orders", description="Operations on orders")

@blp.route("/",methods=['GET'])
def index():
  return { "oi": "oi"}, 200
