import datetime
from odyssey import db
from odyssey.v1.common.constants import GOLF_COURSE_PROFILE, SLOT_PRICING_INFO, SEASONS_INFO, SLOT_TYPE_INFO


class SlotPricingInfo(db.Model):
    __tablename__ = SLOT_PRICING_INFO
    __bind_key__ = 'DATABASE_V1_URI'
    id = db.Column(db.String, primary_key=True)
    slot_type = db.Column(db.String,db.ForeignKey('{}.id'.format(SLOT_TYPE_INFO)))
    season_id = db.Column(db.String,db.ForeignKey('{}.id'.format(SEASONS_INFO)))
    hole_eighteen_price = db.Column(db.Float)
    hole_nine_price = db.Column(db.Float)
    gc_id = db.Column(db.String,db.ForeignKey('{}.id'.format(GOLF_COURSE_PROFILE)))
    status = db.Column(db.String)
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('uuid')
        self.slot_type = kwargs.get('slot_type')
        self.season_id = kwargs.get('season_id')
        self.hole_eighteen_price = kwargs.get('hole_eighteen_price')
        self.hole_nine_price = kwargs.get('hole_nine_price')
        self.status = kwargs.get('status')
        self.gc_id = kwargs.get('gc_id')

