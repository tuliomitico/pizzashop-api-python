from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from marshmallow import fields
 
from ...schemas import ma
from ...db.schema import Restaurants
from ..authentication import jwt_required_with_doc

class UpdateProfileSchema(ma.Schema):
  name = fields.String()
  description = fields.String(required=False)

update_profile_blp = Blueprint("update_profile", "update_profile", url_prefix="/profile", description="Operations on profile")

@update_profile_blp.route("",methods=['PUT'])
@update_profile_blp.arguments(UpdateProfileSchema,location='json')
@jwt_required_with_doc(locations=['cookies'])
def index(body):
    restaurant = get_jwt()
    print(restaurant)
    restaurant_id = restaurant['restaurant_id']

    managed_restaurant: Restaurants = Restaurants.query.filter_by(id=restaurant_id).one_or_none()

    managed_restaurant.user = body['name']
    managed_restaurant.description = body['description']

    return '', 204