import datetime
from odyssey import db
from odyssey.v1.common.constants import CITIES_MASTER, COUNTRIES_MASTER, STATES_MASTER


class CitiesMaster(db.Model):
    __tablename__ = CITIES_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    country_id = db.Column(db.String,db.ForeignKey('{}.id'.format(COUNTRIES_MASTER)))
    state_id =  db.Column(db.String,db.ForeignKey('{}.id'.format(STATES_MASTER)))


    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.country_id = kwargs.get('country_id')
        self.state_id = kwargs.get('state_id')

