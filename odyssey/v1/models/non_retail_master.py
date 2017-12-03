import datetime
from odyssey import db
from odyssey.v1.common.constants import NON_RETAIL_MASTER, VENDOR_MASTER


class NonRetailMaster(db.Model):
    __tablename__ = NON_RETAIL_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    v_id = db.Column(db.String,db.ForeignKey('{}.id'.format(VENDOR_MASTER)))
    created_on = db.Column(db.DateTime,default=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.v_id = kwargs.get('v_id')
        self.created_on = kwargs.get('created_on')

