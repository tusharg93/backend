import datetime
from odyssey import db
from odyssey.v1.common.constants import SLOTS_KEY_COPY


class SlotsKeyCopy(db.Model):
    __tablename__ = SLOTS_KEY_COPY
    __bind_key__ = 'slots_db'
    id = db.Column(db.String, autoincrement=True,primary_key=True)
    gc_id = db.Column(db.String, unique= True,nullable=True)
    is_deleted = db.Column(db.Boolean, default = False)

    def __init__(self, *args, **kwargs):
        self.gc_id = kwargs.get('gc_id')


