import datetime
from odyssey import db
from odyssey.v1.common.constants import COUPON_CATEGORY_MASTER


class CouponCategoryMaster(db.Model):
    __tablename__ = COUPON_CATEGORY_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
