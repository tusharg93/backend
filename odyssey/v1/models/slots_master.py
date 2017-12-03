from odyssey import db
import datetime
from odyssey.v1.common.constants import SLOTS_MASTER, GOLF_COURSE_MASTER, SEASON_MASTER, STATUS_MASTER,CATEGORY_MASTER
class SlotsMaster(db.Model):
    __tablename__ = SLOTS_MASTER
    __bind_key__ = 'base_db'

    # @declared_attr
    # def __table_args__(cls):
    #     return {'schema': _find_schema(cls)}

    id = db.Column(db.String, primary_key=True)
    tee_time = db.Column(db.DateTime)
    date  =  db.Column(db.DateTime)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    slot_category_id = db.Column(db.String,db.ForeignKey('{}.id'.format(CATEGORY_MASTER)))
    t1_avl = db.Column(db.Boolean)
    t10_avl = db.Column(db.Boolean)
    t19_avl = db.Column(db.Boolean)
    rack_rate = db.Column(db.Float)
    season_id = db.Column(db.String,db.ForeignKey('{}.id'.format(SEASON_MASTER)))
    slot_status_id =  db.Column(db.String,db.ForeignKey('{}.id'.format(STATUS_MASTER)))
    created_on  =   db.Column(db.DateTime,default=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.tee_time = kwargs.get('tee_time')
        self.date = kwargs.get('date')
        self.gc_id    = kwargs.get('gc_id')
        self.slot_category_id = kwargs.get('category_id')
        self.t1_avl = kwargs.get('t1_avl')
        self.t10_avl = kwargs.get('t10_avl')
        self.t19_avl = kwargs.get('t19_avl')
        self.rack_rate = kwargs.get('rack_rate')
        self.season_id = kwargs.get('season_id')
        self.slot_status_id = kwargs.get('status_id')
