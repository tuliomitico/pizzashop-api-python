from flask_smorest import Blueprint
from flask import make_response

from flask_jwt_extended import unset_access_cookies

signout_blp = Blueprint("signout", "signout", url_prefix="/sign-out", description="Operations on logout")

@signout_blp.route("",methods=['POST'])
def index():
    response = make_response()
    unset_access_cookies(response)
    return response, 200
