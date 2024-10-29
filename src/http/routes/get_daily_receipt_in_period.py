from datetime import datetime,date, timedelta

from flask_jwt_extended import get_jwt
from flask_smorest import Blueprint
from sqlalchemy import func, and_
from marshmallow import fields

from ..authentication import jwt_required_with_doc
from ...schemas import ma
from ...db.schema import Orders  

class DailyReceiptBodySchema(ma.Schema):
  fromDate = fields.String(allow_none=True)
  to = fields.String(allow_none=True)
  

class ReceiptPerDaySchema(ma.Schema):
  date = fields.String(attribute='date')
  receipt = fields.Number(attribute='receipt')

daily_receipt_blp = Blueprint("daily_receipt", "daily_receipt", url_prefix="/metrics/daily-receipt-in-period", description="Operations on dashboard")

@daily_receipt_blp.route("",methods=['GET'])
@daily_receipt_blp.arguments(DailyReceiptBodySchema,location='query')
@jwt_required_with_doc(locations=['cookies'])
def index(query: DailyReceiptBodySchema):
  restaurant = get_jwt()
  restaurant_id = restaurant['restaurant_id']

  fromDate = query.get('fromDate')
  to = query.get('to')

  if not restaurant_id:
    return {"error":"User is not a restaurant manager"}, 401

  startDate = datetime.fromisoformat(fromDate.replace('Z','+00:00')) if fromDate else datetime.now() - timedelta(days=7)
  endDate = datetime.fromisoformat(to.replace('Z','+00:00')) if to else datetime.now() + timedelta(days=7) if fromDate else datetime.now()  

  if endDate.day - startDate.day > 7:
    return { "code": "INVALID_PERIOD","error":"Invalid date range"}, 400

  receipts_per_day: list[ReceiptPerDaySchema] = Orders.query.with_entities(
    func.to_char(Orders.created_at,'DD/MM').label('date'),
    func.sum(Orders.total_in_cents).label('receipt')
  ).filter(and_(Orders.restaurant_id==restaurant_id,Orders.created_at >= startDate,Orders.created_at <= endDate)).group_by(
    func.to_char(Orders.created_at,"DD/MM")
  ).having(
    func.sum(Orders.total_in_cents) >= 1
  )

  result = ReceiptPerDaySchema().dump(receipts_per_day,many=True)

  ordered_receipt_per_day = sorted(result, key=lambda k: k['date'])

  return ordered_receipt_per_day, 200
