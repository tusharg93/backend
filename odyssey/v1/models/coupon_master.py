import datetime
from odyssey import db
from odyssey.v1.common.constants import COUPON_MASTER, COUPON_CATEGORY_MASTER, VENDOR_MASTER


class CouponMaster(db.Model):
    __tablename__ = COUPON_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    cc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(COUPON_CATEGORY_MASTER)))
    multi_use = db.Column(db.Boolean)
    max_use = db.Column(db.Integer)
    expires_on = db.Column(db.DateTime)
    created_on = db.Column(db.DateTime,default=datetime.datetime.now)
    v_id =  db.Column(db.String,db.ForeignKey('{}.id'.format(VENDOR_MASTER)))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.cc_id = kwargs.get('cc_id')
        self.multi_use = kwargs.get('multi_use')
        self.expires_on = kwargs.get('expires_on')
        self.created_on = kwargs.get('created_on')
        self.v_id = kwargs.get('v_id')
