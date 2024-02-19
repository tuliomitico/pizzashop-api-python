import typing as t


from cuid2 import cuid_wrapper
from flask import request
from flask_smorest import Blueprint
from marshmallow import fields


from .errors.unauthorized_error import UnauthorizedError
from ...schemas import ma
from ...db.schema import User, AuthLinks

cuid_generator = cuid_wrapper()

class BodySchema(ma.Schema):
  email = fields.Email()

auth_blp = Blueprint("authenticate", "authenticate", url_prefix="/authenticate", description="Operations on auth")

@auth_blp.route("",methods=['POST'])
@auth_blp.arguments(BodySchema,location='json')
def index(body):
  user_from_email: t.Union[None,User] = User.query.filter_by(email=body["email"]).first()
  if not user_from_email:
    raise UnauthorizedError()
  
  auth_link_code = cuid_generator()

  AuthLinks(user_id= user_from_email.id, code= auth_link_code).create()

  authlink = f"http://localhost:3333/auth-links/authenticate?code={auth_link_code}&redirect={request.environ.get('HTTP_ORIGIN',None)}"
  print(authlink)
  return '', 200
