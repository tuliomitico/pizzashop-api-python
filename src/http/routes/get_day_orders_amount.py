from datetime import datetime, timedelta

from flask_jwt_extended import get_jwt
from flask_smorest import Blueprint
from sqlalchemy import func, and_
from marshmallow import fields

from ..authentication import jwt_required_with_doc
from ...schemas import ma
from ...db.schema import Orders  

class DayOrderSchema(ma.Schema):
  dayWithMonthAndYear = fields.Date(format='%Y-%m-%d',attribute='dayWithMonthAndYear')
  amount = fields.Number(attribute='amount')

day_order_blp = Blueprint("day_orders", "day_orders", url_prefix="/metrics/day-orders-amount", description="Operations on dashboard")

@day_order_blp.route("",methods=['GET'])
@jwt_required_with_doc(locations=['cookies'])
def index():
  restaurant = get_jwt()
  restaurant_id = restaurant['restaurant_id']

  if not restaurant_id:
    return {"error":"User is not a restaurant manager"}, 401
  
  today = datetime.now()
  yesterday = today - timedelta(days=1)
  start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

  yesterday_with_month_and_year = start_of_yesterday.strftime("%Y-%m-%d")
  today_with_month_and_year = today.strftime("%Y-%m-%d")

  orders_per_day: list[DayOrderSchema] = Orders.query.with_entities(
    func.date_trunc('day', Orders.created_at).label('dayWithMonthAndYear'),
    func.count(Orders.id).label('amount')
  ).filter(and_(Orders.restaurant_id==restaurant_id,Orders.created_at >= start_of_yesterday)).group_by(
    func.date_trunc('day', Orders.created_at)
  ).having(
    func.count(Orders.id) >= 1
  )

  orders = DayOrderSchema().dump(orders_per_day,many=True)

  today_orders_amount = None
  yesterday_orders_amount = None
  
  for order in orders:
    if order['dayWithMonthAndYear'] == today_with_month_and_year:
      today_orders_amount = order
    if order['dayWithMonthAndYear'] == yesterday_with_month_and_year:
      yesterday_orders_amount = order


  diff_from_yesterday = today_orders_amount.get('amount', 1) * 100 / yesterday_orders_amount.get('amount',1) if yesterday_orders_amount and yesterday_orders_amount else None

  result = {
    "amount": today_orders_amount['amount'] if today_orders_amount['amount'] else 0,
    "diffFromYesterday":  "%.2f" % (diff_from_yesterday - 100) if diff_from_yesterday else 0
  }

  return result, 200
