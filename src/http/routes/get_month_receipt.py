from datetime import datetime, timedelta

from flask_jwt_extended import get_jwt
from flask_smorest import Blueprint
from sqlalchemy import func, and_
from marshmallow import fields

from ..authentication import jwt_required_with_doc
from ...schemas import ma
from ...db.schema import Orders  
from ...db.connection import engine

class MonthOrderSchema(ma.Schema):
  monthWithYear = fields.String(attribute='monthWithYear')
  receipt = fields.Number(attribute='receipt')

month_receipt_blp = Blueprint("month_receipt", "month_receipt", url_prefix="/metrics/month-receipt", description="Operations on dashboard")

@month_receipt_blp.route("",methods=['GET'])
@jwt_required_with_doc(locations=['cookies'])
def index():
  restaurant = get_jwt()
  restaurant_id = restaurant['restaurant_id']

  if not restaurant_id:
    return {"error":"User is not a restaurant manager"}, 401
  
  today = datetime.now()
  last_month = today - timedelta(days=30)
  start_of_last_month = last_month.replace(hour=0, minute=0, second=0, microsecond=0, day=1)

  last_month_with_year = start_of_last_month.strftime("%Y-%m")
  current_month_with_year = today.strftime("%Y-%m")

  months_receipts: list[MonthOrderSchema] = Orders.query.with_entities(
    func.to_char(Orders.created_at,'YYYY-MM').label('monthWithYear'),
    func.sum(Orders.total_in_cents).label('receipt')
  ).filter(and_(Orders.restaurant_id==restaurant_id,Orders.created_at >= start_of_last_month)).group_by(
    func.to_char(Orders.created_at,'YYYY-MM')
  ).having(
    func.sum(Orders.total_in_cents) >= 1
  )
  sql_statement = months_receipts.statement.compile(engine, compile_kwargs={"literal_binds": True}).string
  print(sql_statement)
  orders = MonthOrderSchema().dump(months_receipts,many=True)
  print(orders)

  current_month_receipt = None
  last_month_receipt = None
  
  for order in orders:
    if order['monthWithYear'] == current_month_with_year:
      current_month_receipt = order
    if order['monthWithYear'] == last_month_with_year:
      last_month_receipt = order


  diff_from_last_month = current_month_receipt['receipt'] * 100 / last_month_receipt['receipt'] if current_month_receipt and last_month_receipt else None

  result = {
    "receipt": current_month_receipt['receipt'] if current_month_receipt['receipt'] else 0,
    "diffFromLastMonth":  "%.2f" % (diff_from_last_month - 100) if diff_from_last_month else 0
  }

  return result, 200
