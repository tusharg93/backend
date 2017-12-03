from odyssey import db
from odyssey.v1.common.constants import LOGIN_SESSIONS


class LoginSessions(db.Model):
    __tablename__ = LOGIN_SESSIONS
    __bind_key__ = 'base_db'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True)
    data = db.Column(db.LargeBinary)
    expiry = db.Column(db.DateTime)

    def __init__(self, session_id, data, expiry):
        self.session_id = session_id
        self.data = data
        self.expiry = expiry
