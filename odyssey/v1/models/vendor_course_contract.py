import datetime
from odyssey import db
from odyssey.v1.common.constants import VENDOR_COURSE_CONTRACT, GOLF_COURSE_MASTER, VENDOR_MASTER


class VendorCourseContract(db.Model):
    __tablename__ = VENDOR_COURSE_CONTRACT
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    v_id = db.Column(db.String,db.ForeignKey('{}.id'.format(VENDOR_MASTER)))
    request_by = db.Column(db.String)
    request_status = db.Column(db.String,default="PENDING")
    created_on = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    last_updated_on = db.Column(db.DateTime,onupdate=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.gc_id = kwargs.get('gc_id')
        self.v_id = kwargs.get('v_id')
        self.request_by = kwargs.get('request_by')