import datetime
from odyssey import db
from odyssey.v1.common.constants import TRANSACTIONS_MASTER, GOLF_COURSE_MASTER, SEASON_MASTER, VENDOR_MASTER, NON_RETAIL_MASTER


class TransactionsMaster(db.Model):
    __tablename__ = TRANSACTIONS_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    date  =  db.Column(db.DateTime,default = datetime.datetime.utcnow)
    gc_id = db.Column(db.String,db.ForeignKey('{}.gc_id'.format(GOLF_COURSE_MASTER)))
    season_id = db.Column(db.String,db.ForeignKey('{}.season_id'.format(SEASON_MASTER)))
    v_id = db.Column(db.String,db.ForeignKey('{}.v_id'.format(VENDOR_MASTER)))
    amount = db.Column(db.Float)
    tc_id  = db.Column(db.String)
    ts_id = db.Column(db.String)
    user_details_1 = db.Column(db.String)
    user_details_2 = db.Column(db.String)
    user_details_3 = db.Column(db.String)
    user_details_4 = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    nr_id = db.Column(db.String,db.ForeignKey('{}.non_retail_id'.format(NON_RETAIL_MASTER)))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.tee_time = kwargs.get('tee_time')
        self.date = kwargs.get('date')
        self.gc_id    = kwargs.get('gc_id')
        self.category_id = kwargs.get('category_id')
        self.t1_avl = kwargs.get('t1_avl')
        self.t10_avl = kwargs.get('t10_avl')
        self.t19_avl = kwargs.get('t19_avl')
        self.rack_rate = kwargs.get('rack_rate')
        self.season_id = kwargs.get('season_id')
        self.status_id = kwargs.get('status_id')
