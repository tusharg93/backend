import datetime
from odyssey import db
from odyssey.v1.common.constants import COURSE_SEASON_RATES, GOLF_COURSE_MASTER, SEASON_MASTER


class CourseSeasonRates(db.Model):
    __tablename__ = COURSE_SEASON_RATES
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    season_id = db.Column(db.String,db.ForeignKey('{}.id'.format(SEASON_MASTER)))
    gc_id = db.Column(db.String,db.ForeignKey('{}.gc_id'.format(GOLF_COURSE_MASTER)))
    updated_on = db.Column(db.DateTime,onupdate=datetime.datetime.now)
    created_on = db.Column(db.DateTime,default=datetime.datetime.now)
    discount_rate = db.Column(db.Float)


    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.season_id = kwargs.get('season_id')
        self.gc_id = kwargs.get('gc_id')
        self.updated_on = kwargs.get('updated_on')
        self.discount_rate = kwargs.get('discount_rate')


