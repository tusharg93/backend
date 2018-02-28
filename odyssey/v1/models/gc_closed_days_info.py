from odyssey import db
from sqlalchemy.dialects.postgresql import TIME, DATE
from odyssey.v1.common.constants import GC_CLOSED_DAYS_INFO, DAYS_TYPE_INFO, GOLF_COURSE_MASTER, SEASON_MASTER


class GCClosedDaysInfo(db.Model):
    __tablename__ = GC_CLOSED_DAYS_INFO
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    date = db.Column(db.Date)
    full_day = db.Column(db.Boolean,default=False)
    start_time = db.Column(TIME())
    end_time = db.Column(TIME())

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.gc_id = kwargs.get('gc_id')
        self.date  = kwargs.get('date')
        self.full_day = kwargs.get('full_day')
        self.start_time = kwargs.get('start_time')


    @property
    def closed_serialize(self):
        return {
            "id":self.id,
            "date":self.date.strftime('%Y-%m-%d'),
            "full_day":self.full_day,
            "start_time":self.start_time.strftime('%H:%M') if self.start_time else None

        }


