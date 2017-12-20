from odyssey import db
import datetime
from pytz import timezone
from sqlalchemy.dialects.postgresql import TIME
from odyssey.v1.common.constants import SLOTS_MASTER, GOLF_COURSE_MASTER, SEASON_MASTER, STATUS_MASTER,CATEGORY_MASTER
class SlotsMaster(db.Model):
    __tablename__ = SLOTS_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    tee_time = db.Column(TIME())
    date  =  db.Column(db.Date)
    hole_9_price = db.Column(db.Float)
    hole_18_price = db.Column(db.Float)
    season_id = db.Column(db.String)
    day_type = db.Column(db.String)
    slot_status = db.Column(db.String)
    min_golfers = db.Column(db.Integer)

class SlotObject(object):
    def __init__(self, slot_object):
        self.id = slot_object['id']
        self.tee_time = slot_object['tee_time']
        self.date = slot_object['date']
        self.hole_9_price = slot_object['hole_9_price']
        self.hole_18_price = slot_object['hole_18_price']
        self.season_id = slot_object['season_id']
        self.day_type = slot_object['day_type']
        self.slot_status = slot_object['slot_status']
        self.min_golfers = slot_object['min_golfers']