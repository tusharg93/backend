import datetime
from odyssey import db
from odyssey.v1.common.constants import GOLF_COURSE_PROFILE, CURRENCY_INFO


class GolfCourseProfile(db.Model):
    __tablename__ = GOLF_COURSE_PROFILE
    __bind_key__ = 'DATABASE_V1_URI'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    currency_id = db.Column(db.String,db.ForeignKey('{}.id'.format(CURRENCY_INFO)))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('uuid')
        self.name = kwargs.get('name')
        self.address = kwargs.get('address')
        self.state = kwargs.get('state')
        self.country = kwargs.get('country')
        self.currency_id = kwargs.get('currency_id')

