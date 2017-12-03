import datetime
from odyssey import db
from odyssey.v1.common.constants import COURSE_IMAGES_MASTER, GOLF_COURSE_MASTER


class CourseImageMaster(db.Model):
    __tablename__ = COURSE_IMAGES_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    seq = db.Column(db.Integer)
    url = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.gc_id = kwargs.get('gc_id')
        self.seq = kwargs.get('seq')
        self.url = kwargs.get('url')
