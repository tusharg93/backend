import datetime
from odyssey import db
from odyssey.v1.common.constants import GOLF_COURSE_USER_PROFILE, GOLF_COURSE_PROFILE


class GolfCourseUserProfile(db.Model):
    __tablename__ = GOLF_COURSE_USER_PROFILE
    __bind_key__ = 'DATABASE_V1_URI'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    mobile = db.Column(db.String)
    country_code = db.Column(db.String)
    password = db.Column(db.String)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_PROFILE)))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('uuid')
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.mobile = kwargs.get('mobile')
        self.country_code = kwargs.get('country_code')
        self.password = kwargs.get('password')
        self.gc_id = kwargs.get('gc_id')

