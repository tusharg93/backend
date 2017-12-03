import datetime
from odyssey import db
from odyssey.v1.common.constants import REGIONS_MASTER


class RegionsMaster(db.Model):
    __tablename__ = REGIONS_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    countries =  db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.countries = kwargs.get('countries')