from flask_smorest import Blueprint
from flask_jwt_extended import  jwt_required, get_jwt


from ...db.schema import Restaurants

restaurant_blp = Blueprint("managed_restaurant", "managed_restaurant", url_prefix="/managed-restaurant", description="Operations on restaurant")

@restaurant_blp.route("",methods=['GET'])
@jwt_required(locations=['cookies'])
def index():
    restaurant = get_jwt()
    print(restaurant)
    restaurant_id = restaurant['restaurant_id']

    managed_restaurant: Restaurants = Restaurants.query.filter_by(id=restaurant_id).one_or_none()  
    return {
        "id": managed_restaurant.id,
        "name": managed_restaurant.name,
        "description": managed_restaurant.description,
        "managerId": managed_restaurant.manager_id,
        "createdAt": managed_restaurant.created_at,
        "updatedAt": managed_restaurant.updated_at
     }, 200