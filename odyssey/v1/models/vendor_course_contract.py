import datetime
from odyssey import db
from odyssey.v1.common.constants import VENDOR_COURSE_CONTRACT, GOLF_COURSE_MASTER, VENDOR_MASTER


class VendorCourseContract(db.Model):
    __tablename__ = VENDOR_COURSE_CONTRACT
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    v_id = db.Column(db.String,db.ForeignKey('{}.id'.format(VENDOR_MASTER)))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    rack_rate_avl = db.Column(db.Boolean)
    retail_wkday_cmsn = db.Column(db.Float)
    retail_wkend_cmsn = db.Column(db.Float)
    corporate_avl = db.Column(db.Boolean)
    corp_wkday_Cmsn = db.Column(db.Float)
    corp_wkend_cmsn = db.Column(db.Float)

    def __init__(self, *args, **kwargs):

        self.id = kwargs.get('id')
        self.gc_id = kwargs.get('gc_id')
        self.vc_id = kwargs.get('vc_id')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')
        self.retail_wkday_cmsn = kwargs.get('retail_wkday_cmsn')
        self.retail_wkend_cmsn = kwargs.get('retail_wkend_cmsn')
        self.corporate_avl = kwargs.get('corporate_avl')
        self.corp_wkday_Cmsn = kwargs.get('corp_wkday_Cmsn')
        self.corp_wkend_cmsn = kwargs.get('corp_wkend_cmsn')
