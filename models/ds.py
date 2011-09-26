from google.appengine.ext import db
from google.appengine.ext import blobstore

from datetime import datetime
from pytz.gae import pytz
from pytz import timezone

class Booking(db.Model):
  last_date = db.DateProperty(default=datetime.now(timezone('Australia/Sydney')).date())

  def to_dict(self):
    return {
           'credit_expiry': self.credit_expiry,
           }
