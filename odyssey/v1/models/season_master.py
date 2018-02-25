import datetime
from odyssey import db
from odyssey.v1.common.constants import SEASON_MASTER


class SeasonsMaster(db.Model):
    __tablename__ = SEASON_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')

    @property
    def season_serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }