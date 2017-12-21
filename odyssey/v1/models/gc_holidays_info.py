import datetime
from odyssey import db
from odyssey.v1.common.constants import GC_HOLIDAYS_DAYS_INFO, GOLF_COURSE_MASTER


class GCHolidaysDaysInfo(db.Model):
    __tablename__ = GC_HOLIDAYS_DAYS_INFO
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    date = db.Column(db.Date)
    name = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.date = kwargs.get('date')
        self.gc_id   =   kwargs.get('gc_id')
        self.name = kwargs.get('name')




