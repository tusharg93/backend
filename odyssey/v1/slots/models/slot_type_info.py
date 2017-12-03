import datetime
from odyssey import db
from odyssey.v1.common.constants import GOLF_COURSE_PROFILE, SLOT_TYPE_INFO, DAYS_INFO


class SlotTypeInfo(db.Model):
    __tablename__ = SLOT_TYPE_INFO
    __bind_key__ = 'DATABASE_V1_URI'
    id = db.Column(db.String, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    start_day = db.Column(db.String,db.ForeignKey('{}.id'.format(DAYS_INFO)))
    end_day = db.Column(db.String,db.ForeignKey('{}.id'.format(DAYS_INFO)))
    status = db.Column(db.String)
    holes = db.Column(db.Integer)
    time_interval = db.Column(db.Integer)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_PROFILE)))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('uuid')
        self.start_time = kwargs.get('start_time')
        self.end_time = kwargs.get('end_time')
        self.time_interval = kwargs.get('time_interval')
        self.status = kwargs.get('status')
        self.start_day = kwargs.get('start_day')
        self.end_day = kwargs.get('end_day')
        self.holes = kwargs.get('holes')
        self.gc_id = kwargs.get('gc_id')

