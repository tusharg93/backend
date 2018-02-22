import datetime
from odyssey import db
from odyssey.v1.common.constants import GC_RATES_INFO, GOLF_COURSE_MASTER, SEASON_MASTER, DAYS_TYPE_INFO, RATE_TYPE


class GCRatesInfo(db.Model):
    __tablename__ = GC_RATES_INFO
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    season_id = db.Column(db.String,db.ForeignKey('{}.id'.format(SEASON_MASTER)))
    day_type = db.Column(db.String,db.ForeignKey('{}.id'.format(DAYS_TYPE_INFO)))
    hole_9_price = db.Column(db.Float)
    hole_18_price = db.Column(db.Float)
    rate_type = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.gc_id = kwargs.get('gc_id')
        self.season_id = kwargs.get('season_id')
        self.day_type = kwargs.get('day_type')
        self.rate_type = kwargs.get('rate_type')
        self.hole_9_price = kwargs.get('hole_9_price')
        self.hole_18_price = kwargs.get('hole_18_price')

