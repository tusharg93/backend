import datetime
from odyssey import db
from sqlalchemy.dialects.postgresql import TIME, DATE
from odyssey.v1.common.constants import GC_SPECIAL_DAYS_INFO, DAYS_TYPE_INFO, GOLF_COURSE_MASTER


class GCSpecialDaysInfo(db.Model):
    __tablename__ = GC_SPECIAL_DAYS_INFO
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    day_type = db.Column(db.String,db.ForeignKey('{}.id'.format(DAYS_TYPE_INFO)))
    day = db.Column(db.String)
    full_day = db.Column(db.Boolean,default=True)
    start_time = db.Column(TIME())
    end_time = db.Column(TIME())

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.day_type = kwargs.get('day_type')
        self.day   =   kwargs.get('day')
        self.full_day = kwargs.get('full_day')
        self.start_time = kwargs.get('start_time')
        self.end_time = kwargs.get('end_time')



