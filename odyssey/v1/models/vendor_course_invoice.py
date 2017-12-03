import datetime
from odyssey import db
from odyssey.v1.common.constants import VENDOR_COURSE_INVOICE, GOLF_COURSE_MASTER, VENDOR_MASTER


class VendorCourseInvoice(db.Model):
    __tablename__ = VENDOR_COURSE_INVOICE
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    v_id = db.Column(db.String,db.ForeignKey('{}.id'.format(VENDOR_MASTER)))
    inv_value = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    pay_by_date = db.Column(db.DateTime)
    status = db.Column(db.String)
    pay_mode = db.Column(db.String)
    details = db.Column(db.String)
    flagged_cr = db.Column(db.Boolean)
    flagged_vn = db.Column(db.Boolean)
    flag_desc_cr = db.Column(db.String)
    flag_desc_vn = db.Column(db.String)


    def __init__(self, *args, **kwargs):
            self.id = kwargs.get('id')
            self.gc_id = kwargs.get('gc_id')
            self.v_id = kwargs.get('v_id')
            self.inv_value = kwargs.get('inv_value')
            self.create_date = kwargs.get('create_date')
            self.pay_by_date = kwargs.get('pay_by_date')
            self.status = kwargs.get('status')
            self.pay_mode = kwargs.get('pay_mode')
            self.details = kwargs.get('details')
            self.flagged_cr = kwargs.get('flagged_cr')
            self.flagged_vn = kwargs.get('flagged_vn')
            self.flag_desc_cr = kwargs.get('flag_desc_cr')
            self.flag_desc_vn = kwargs.get('flag_desc_vn')
