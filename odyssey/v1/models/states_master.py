import datetime
from odyssey import db
from odyssey.v1.common.constants import STATES_MASTER, COUNTRIES_MASTER


class StatesMaster(db.Model):
    __tablename__ = STATES_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    country_id = db.Column(db.String,db.ForeignKey('{}.id'.format(COUNTRIES_MASTER)))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.country_id = kwargs.get('country_id')

