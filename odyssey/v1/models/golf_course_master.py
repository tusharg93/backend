import datetime
from odyssey import db, app
from pytz import timezone
from odyssey.v1.common.constants import GOLF_COURSE_MASTER
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.dialects.postgresql import JSON
from itsdangerous import URLSafeSerializer
login_serializer = URLSafeSerializer(app.secret_key)

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
    description = db.Column(JSON)
    address_1 = db.Column(db.String)
    address_2  = db.Column(db.String)
    lat = db.Column(db.String)
    long = db.Column(db.String)
    logo_url = db.Column(db.String)
    facilities = db.Column(JSON)
    weekday_hrs = db.Column(db.String)
    weekend_hrs = db.Column(db.String)
    course_info = db.Column(JSON)
    contact_name = db.Column(db.String)
    contact_mobile = db.Column(db.String)
    contact_country_code = db.Column(db.String)
    website_url = db.Column(db.String)
    facebook_url = db.Column(db.String)
    twitter_url  = db.Column(db.String)
    insta_url = db.Column(db.String)
    email = db.Column(db.String)
    min_weekdays = db.Column(db.Integer)
    min_weekends = db.Column(db.Integer)
    cancel_policy = db.Column(db.String)
    tnc         = db.Column(db.String)
    price_includes = db.Column(JSON)
    auth_token = db.Column(db.String)
    maintenance_day = db.Column(db.String)
    maintenance_type = db.Column(db.Boolean)
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
        self.hash_password(kwargs.get('password'))
        self.email = kwargs.get('email')
        #self.created_on = kwargs.get('created_on')

    @property
    def dashboard_serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "is_hole_9":self.hole_9_flag,
            "is_hole_18":self.hole_18_flag,
            "tee_avl":self.tee_avl,
            "currency":self.currency,
            "time_zone":self.time_zone,
            "online":self.is_online,
            "member":self.is_member,
            "guest":self.is_guest,
            "live_slots_duration":self.duration_live_slots,
            "weekdays":self.weekdays,
            "weekends":self.weekends,
            "maintenance_day":self.maintenance_day,
            "maintenance_type":self.maintenance_type,
            "min_golfers_weekends":self.min_weekends,
            "min_golfers_weekdays":self.min_weekdays,
            "insta_url":self.insta_url,
            "twiter_url":self.twitter_url,
            "facebook_url":self.facebook_url,
            "facilities":self.facilities,
            "logo_url":self.logo_url,
            "address_line_2":self.address_2,
            "address_line_1":self.address_1,
            "person_mobile":self.contact_mobile,
            "person_name":self.contact_name,
            "website_url":self.website_url,
            "course_info":self.course_info,
            "weekday_operating_hrs":self.weekday_hrs,
            "weekend_operating_hrs":self.weekend_hrs,
            "mobile":self.mobile,
            "country_code":self.country_code
        }

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_auth_token(self):
        data = [self.password, self.email]
        return login_serializer.dumps(data)

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
