import datetime
from odyssey import db
from odyssey.v1.common.constants import DAYS_TYPE_INFO


class DaysTypeInfo(db.Model):
    __tablename__ = DAYS_TYPE_INFO
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    day_type = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.day_type = kwargs.get('day_type')

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.day_type
        }
