import datetime
from odyssey import db
from odyssey.v1.common.constants import TRANS_KEY_COPY


class TransKeyCopy(db.Model):
    __tablename__ = TRANS_KEY_COPY
    __bind_key__ = 'base_db'
    id = db.Column(db.String, autoincrement=True, primary_key=True)
    gc_id = db.Column(db.String,  nullable= True, unique=True)
    v_id = db.Column(db.String, nullable = True, unique=True)
    season_id = db.Column(db.String, nullable = True, unique=True)
    non_retail_id = db.Column(db.String, nullable = True, unique=True)
    is_deleted = db.Column(db.Boolean, default = False)

    def __init__(self, *args, **kwargs):
        self.gc_id = kwargs.get('gc_id')
        self.season_id = kwargs.get('season_id')
        self.v_id = kwargs.get('v_id')
        self.non_retail_id = kwargs.get('non_retail_id')



