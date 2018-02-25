import datetime
from odyssey import db
from odyssey.v1.common.constants import GC_SEASONS_INFO, GOLF_COURSE_MASTER, SEASON_MASTER
from sqlalchemy.dialects.postgresql import TIME,DATE

class GCSeasonsInfo(db.Model):
    __tablename__ = GC_SEASONS_INFO
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    season_id = db.Column(db.String,db.ForeignKey('{}.id'.format(SEASON_MASTER)))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    start_time = db.Column(TIME())
    end_time = db.Column(TIME())
    tee_interval = db.Column(db.Integer)


    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.gc_id = kwargs.get('gc_id')
        self.season_id = kwargs.get('season_id')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')
        self.start_time = kwargs.get('start_time')
        self.end_time = kwargs.get('end_time')
        self.tee_interval = kwargs.get('tee_interval')

    @property
    def gc_season_serialize(self):
        import time
        from datetime import datetime
        return {
            "id": self.id,
            "start_date":datetime.strftime(self.start_date,"%m-%d",) if self.start_date else None,
            "end_date":datetime.strftime(self.end_date,"%m-%d") if self.end_date else None,
            "start_time":time.strftime("%H:%M",self.start_time) if self.start_time else None,
            "end_time":time.strftime("%H:%M",self.end_time) if self.end_time else None,
            "tee_interval":self.tee_interval if self.tee_interval else None
        }