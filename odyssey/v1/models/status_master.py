import datetime
from odyssey import db
from odyssey.v1.common.constants import STATUS_MASTER


class StatusMaster(db.Model):
    __tablename__ = STATUS_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')

