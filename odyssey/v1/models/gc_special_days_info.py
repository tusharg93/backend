from odyssey import db
from sqlalchemy.dialects.postgresql import TIME, DATE
from odyssey.v1.common.constants import GC_SPECIAL_DAYS_INFO, DAYS_TYPE_INFO, GOLF_COURSE_MASTER, SEASON_MASTER


class GCSpecialDaysInfo(db.Model):
    __tablename__ = GC_SPECIAL_DAYS_INFO
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    season_id = db.Column(db.String,db.ForeignKey('{}.id'.format(SEASON_MASTER)))
    day_type = db.Column(db.String,db.ForeignKey('{}.id'.format(DAYS_TYPE_INFO)))
    day = db.Column(db.String)
    full_day = db.Column(db.Boolean,default=True)
    start_time = db.Column(TIME())
    end_time = db.Column(TIME())

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.gc_id = kwargs.get('gc_id')
        self.day_type = kwargs.get('day_type')
        self.day   =   kwargs.get('day')
        self.full_day = kwargs.get('full_day') if kwargs.get('full_day') else True


    @property
    def weekly_off_serialize(self):
        import time
        return {
            "id":self.id,
            "day":self.day,
            "season_id":self.season_id,
            "full_day":self.full_day,
            "day_type":self.day_type,
            "start_time":time.strftime('%H:%M',self.start_time) if self.start_time else None,
            "end_time":time.strftime('%H:%M',self.end_time) if self.end_time else None
        }


