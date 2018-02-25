import datetime
from odyssey import db
from odyssey.v1.common.constants import EXTRAS_INFO,  GOLF_COURSE_MASTER


class ExtrasInfo(db.Model):
    __tablename__ = EXTRAS_INFO
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))


    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.gc_id = kwargs.get('gc_id')
        self.price = kwargs.get('price')

    @property
    def extras_serialize(self):
        return {
            "id": self.id,
            "price":self.price,
            "name": self.name
        }