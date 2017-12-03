import datetime

from odyssey import db
from odyssey.v1.common.constants import \
    MEMBER_SESSION_KEYS, \
    GOLF_COURSE_MASTER


class MemberSessionKeys(db.Model):
    __tablename__ = MEMBER_SESSION_KEYS
    __bind_key__ = 'base_db'

    id = db.Column(db.String, primary_key=True)
    member_id = db.Column(db.String, db.ForeignKey('{}.id'.format(GOLF_COURSE_MASTER)))
    session_id = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)
    last_updated_on = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('uuid')
        self.member_id = kwargs.get('member_id')
        self.session_id = kwargs.get('session_id')
