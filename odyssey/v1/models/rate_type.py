import datetime
from odyssey import db
from odyssey.v1.common.constants import RATE_TYPE


class RateType(db.Model):
    __tablename__ = RATE_TYPE
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name":self.name
            }