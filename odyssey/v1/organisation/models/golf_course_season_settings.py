import datetime
from odyssey import db
from odyssey.v1.common.constants import GOLF_COURSE_SEASON_SETTINGS, GOLF_COURSE_PROFILE,SEASONS_INFO


class GolfCourseSeasonSettings(db.Model):
    __tablename__ = GOLF_COURSE_SEASON_SETTINGS
    __bind_key__ = 'DATABASE_V1_URI'
    id = db.Column(db.String, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String)
    season_id = db.Column(db.String,db.ForeignKey('{}.id'.format(SEASONS_INFO)))
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_PROFILE)))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('uuid')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')
        self.status = kwargs.get('status')
        self.season_id = kwargs.get('season_id')
        self.gc_id = kwargs.get('gc_id')

