import datetime
from odyssey import db
from odyssey.v1.common.constants import GOLF_COURSE_GENERAL_SETTINGS, GOLF_COURSE_PROFILE,SEASONS_INFO, EXTRAS_INFO


class GolfCourseGeneralSettings(db.Model):
    __tablename__ = GOLF_COURSE_GENERAL_SETTINGS
    __bind_key__ = 'DATABASE_V1_URI'
    id = db.Column(db.String, primary_key=True)
    type_id = db.Column(db.String,db.ForeignKey('{}.id'.format(EXTRAS_INFO)))
    price = db.Column(db.Float)
    is_free = db.Column(db.Bool)
    status = db.Column(db.String)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_PROFILE)))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('uuid')
        self.type_id = kwargs.get('type_id')
        self.price = kwargs.get('price')
        self.is_free = kwargs.get('is_free')
        self.status = kwargs.get('status')
        self.gc_id = kwargs.get('gc_id')

