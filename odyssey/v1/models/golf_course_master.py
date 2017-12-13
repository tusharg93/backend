import datetime
from odyssey import db
from pytz import timezone
from odyssey.v1.common.constants import GOLF_COURSE_MASTER
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.schema import ForeignKey

class GolfCourseMaster(db.Model):
    __tablename__ = GOLF_COURSE_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    country = db.Column(db.String)
    state =  db.Column(db.String)
    city = db.Column(db.String)
    time_zone =  db.Column(db.String)
    hole_9_flag = db.Column(db.Boolean)
    hole_18_flag = db.Column(db.Boolean)
    weekdays = db.Column(db.String)
    weekends = db.Column(db.String)
    tee_avl = db.Column(db.String)
    is_member = db.Column(db.Boolean)
    is_guest = db.Column(db.Boolean)
    is_online = db.Column(db.Boolean)
    duration_live_slots = db.Column(db.Integer)
    mobile  =   db.Column(db.String)
    country_code = db.Column(db.String)
    description = db.Column(db.String)
    address = db.Column(db.String)
    location = db.Column(db.String)
    logo_url = db.Column(db.String)
    established = db.Column(db.DateTime)
    email = db.Column(db.String)
    is_email_verified = db.Column(db.Boolean,default=False)
    is_deleted     = db.Column(db.Boolean,default=False)
    official_email = db.Column(db.Boolean,default=False)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime,default=datetime.datetime.now(timezone('UTC')))
    activated_on = db.Column(db.DateTime)
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.country = kwargs.get('country')
        #self.state = kwargs.get('state')
        self.city = kwargs.get('city')
        self.mobile = kwargs.get('mobile')
        self.country_code = kwargs.get('country_code')
        #self.holes = kwargs.get('holes')
        #self.t1_avl  = kwargs.get('t1avl')
        #self.t10_avl = kwargs.get('t10avl')
        #self.t19_avl = kwargs.get('t19avl')
        #self.description = kwargs.get('description')
        #self.address = kwargs.get('address')
        #self.location = kwargs.get('location')
        #self.logo_url = kwargs.get('logoUrl')
        #self.par = kwargs.get('par')
        #self.established = kwargs.get('established')
        #self.facilities  = kwargs.get('facilities')
        #self.rate_inclusions = kwargs.get('rateInclusions')
        self.email = kwargs.get('email')
        #self.created_on = kwargs.get('created_on')
        self.hash_password(kwargs.get('password'))


    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def get_default_password(self):
        return str(self.email).strip().lower().split('@')[0]

    def verify_password(self, password):
        try:
            return pwd_context.verify(password, self.password)
        except TypeError:
            return False
        except ValueError:
            return False
