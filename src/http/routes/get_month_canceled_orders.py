from datetime import datetime, timedelta

from flask_jwt_extended import get_jwt
from flask_smorest import Blueprint
from sqlalchemy import func, and_
from marshmallow import fields

from ..authentication import jwt_required_with_doc
from ...schemas import ma
from ...db.schema import Orders  
from ...db.connection import engine

class MonthCanceledOrderSchema(ma.Schema):
    monthWithYear = fields.String(attribute='monthWithYear')
    amount = fields.Number(attribute='amount')

month_canceled_order_blp = Blueprint("month_canceled_orders", "month_canceled_orders",
                            url_prefix="/metrics/month-canceled-orders-amount", 
                            description="Operations on dashboard")

@month_canceled_order_blp.route("",methods=['GET'])
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

  orders_per_month: list[MonthCanceledOrderSchema] = Orders.query.with_entities(
    func.to_char(Orders.created_at,'YYYY-MM').label('monthWithYear'),
    func.count(Orders.id).label('amount')
  ).filter(and_(Orders.restaurant_id==restaurant_id,Orders.created_at >= start_of_last_month)).group_by(
    func.to_char(Orders.created_at,'YYYY-MM')
  ).filter_by(status='canceled').having(
    func.count(Orders.id) >= 1
  )

  orders = MonthCanceledOrderSchema().dump(orders_per_month,many=True)

  current_month_orders_amount = None
  last_month_orders_amount = None
  
  for order in orders:
    if order['monthWithYear'] == current_month_with_year:
      current_month_orders_amount = order
    if order['monthWithYear'] == last_month_with_year:
      last_month_orders_amount = order


  diff_from_last_month = current_month_orders_amount['amount'] * 100 / last_month_orders_amount['amount'] if current_month_orders_amount and last_month_orders_amount else None

  result = {
    "amount": current_month_orders_amount['amount'] if current_month_orders_amount['amount'] else 0,
    "diffFromLastMonth":  "%.2f" % (diff_from_last_month - 100) if diff_from_last_month else 0
  }

  return result, 200
