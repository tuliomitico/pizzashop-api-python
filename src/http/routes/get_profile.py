from flask_smorest import Blueprint
from flask_jwt_extended import get_current_user

from ..authentication import jwt_required_with_doc
from ...db.schema import User

profile_blp = Blueprint("profile", "profile", url_prefix="/me", description="Operations on me")

@profile_blp.route("",methods=['GET'])
@jwt_required_with_doc(locations=['cookies'])
def index():
    user: User = get_current_user()  
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "createdAt": user.created_at,
        "updatedAt": user.updated_at
     }, 200