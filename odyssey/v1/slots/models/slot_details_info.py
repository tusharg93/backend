import datetime
from odyssey import db
from odyssey.v1.common.constants import GOLF_COURSE_PROFILE, SLOT_DETAILS_INFO, SLOT_TYPE_INFO


class SlotDetailsInfo(db.Model):
    __tablename__ = SLOT_DETAILS_INFO
    __bind_key__ = 'DATABASE_V1_URI'
    id = db.Column(db.String, primary_key=True)
    slot_type = db.Column(db.String,db.ForeignKey('{}.id'.format(SLOT_TYPE_INFO)))
    slot_time = db.Column(db.Time)
    status = db.Column(db.String)
    description = db.Column(db.String)
    holes = db.String(db.Integer)
    min_players = db.String(db.Integer)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_PROFILE)))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('uuid')
        self.slot_time = kwargs.get('slot_time')
        self.slot_type = kwargs.get('slot_type')
        self.status = kwargs.get('status')
        self.description = kwargs.get('description')
        self.holes = kwargs.get('holes')
        self.min_players = kwargs.get('min_players')
        self.gc_id = kwargs.get('gc_id')

