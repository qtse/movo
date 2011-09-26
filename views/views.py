###from models.ds import Booking, Passenger, Sector, Document
###from models.ds import PassengerSectorBooking, LastUse

from google.appengine.ext import db

from datetime import datetime, timedelta
from pytz.gae import pytz
from pytz import timezone

# Constants, private functions
_active_period = timedelta(days=90)
_expiry_period = timedelta(days=365*2)

def _current_date():
  return datetime.now(timezone('Australia/Sydney')).date()

def _use(obj_key):
  key_str = str(obj_key)
  now = _current_date()
  u = LastUse.get_or_insert(key_str, obj=obj_key)
  if now > u.last_use:
    u.last_use = now
    db.put_async(u)

# get functions

# By identifiers
def get_booking_by_id(booking_id):
  b = Booking.get_by_id(booking_id)
  if b:
    _use(b.key())
    return b.to_dict()
  return None

