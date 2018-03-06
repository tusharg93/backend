from odyssey import db
import datetime
from pytz import timezone
from sqlalchemy.dialects.postgresql import TIME
from odyssey.v1.common.constants import SLOTS_MASTER, SEASON_MASTER, DAYS_TYPE_INFO
class SlotsMaster(db.Model):
    __tablename__ = SLOTS_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    tee_time = db.Column(TIME())
    date  =  db.Column(db.Date)
    day = db.Column(db.String)
    hole_9_price = db.Column(db.Float)
    hole_18_price = db.Column(db.Float)
    season_id = db.Column(db.String,db.ForeignKey('{}.id'.format(SEASON_MASTER)))
    day_type = db.Column(db.String,db.ForeignKey('{}.id'.format(DAYS_TYPE_INFO)))
    slot_status_9 = db.Column(db.String)
    slot_status_18 = db.Column(db.String)
    min_golfers = db.Column(db.Integer)

