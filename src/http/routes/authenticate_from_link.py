import typing as t
import datetime
from datetime import timedelta


from flask import Response, redirect, request
from flask_smorest import Blueprint
from marshmallow import fields
import jwt


from .errors.unauthorized_error import UnauthorizedError
from ...schemas import ma
from ...db.schema import AuthLinks, Restaurants
from ...db.connection import db_session

class QuerySchema(ma.Schema):
  code = fields.String()
  redirect= fields.Url()

auth_blp = Blueprint("authenticate-link", "authenticate-link", url_prefix="/auth-links/authenticate", description="Operations on authlink")

def sign_user(payload) -> Response:
  response = redirect(request.args.get('redirect'))
  response.set_cookie('auth',jwt.encode({
        "sub": payload['sub'],
        "restaurant_id": payload['restaurant_id'],
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + timedelta(minutes=45)
      },
      "my-super-secret-key",
      algorithm='HS256'),httponly=True,max_age=7 * 86400,path='/')
  return response

@auth_blp.route("",methods=['GET'])
@auth_blp.arguments(QuerySchema,location='query',required=False)
def index(body: QuerySchema):
  auth_link_from_code = AuthLinks.query.filter_by(code=body['code']).one_or_none()
  if not auth_link_from_code:
    raise UnauthorizedError()
  if (datetime.datetime.now() - auth_link_from_code.created_at) > timedelta(days=7):
    raise UnauthorizedError()
  
  managed_restaurant = Restaurants.query.filter_by(manager_id=auth_link_from_code.user_id).one_or_none()
  
  response = sign_user({ "sub":auth_link_from_code.user_id,"restaurant_id":managed_restaurant.id})

  db_session.query(AuthLinks).filter(AuthLinks.user_id == auth_link_from_code.user_id).delete()
  db_session.commit()

  return response