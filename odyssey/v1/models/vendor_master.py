import datetime
from odyssey import db, app
from odyssey.v1.common.constants import VENDOR_MASTER, COUNTRIES_MASTER, CITIES_MASTER
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import URLSafeSerializer
login_serializer = URLSafeSerializer(app.secret_key)

class VendorMaster(db.Model):
    __tablename__ = VENDOR_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    company_name = db.Column(db.String)
    person_name = db.Column(db.String)
    company_country_code = db.Column(db.String)
    person_country_code = db.Column(db.String)
    designation = db.Column(db.String)
    person_contact = db.Column(db.String)
    country   = db.Column(db.String)
    city = db.Column(db.String)
    address_1 = db.Column(db.String)
    address_2 = db.Column(db.String)
    weekday_hrs = db.Column(db.String)
    weekend_hrs = db.Column(db.String)
    twitter_url = db.Column(db.String)
    facebook_url = db.Column(db.String)
    instagram_url = db.Column(db.String)
    linkedin_url = db.Column(db.String)
    gplus_url = db.Column(db.String)
    mobile = db.Column(db.String)
    auth_token = db.Column(db.String)
    logo_url = db.Column(db.String)
    website_url = db.Column(db.String)
    description = db.Column(db.String)
    email = db.Column(db.String)
    is_email_verified = db.Column(db.Boolean,default=False)
    is_deleted = db.Column(db.Boolean,default=False)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    activated_on = db.Column(db.DateTime)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.company_name = kwargs.get('name')
        self.country = kwargs.get('country')
        self.city    = kwargs.get('city')
        self.mobile = kwargs.get('mobile')
        self.website_url = kwargs.get('website_url')
        self.company_country_code = kwargs.get('country_code')
        self.email = kwargs.get('email')
        self.hash_password(kwargs.get('password'))

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
        data = [self.email, self.password_hash]
        return login_serializer.dumps(data)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def get_default_password(self):
        return str(self.email).strip().lower().split('@')[0]

    def verify_password(self, password):
        try:
            return pwd_context.verify(password, self.password_hash)
        except TypeError:
            return False
        except ValueError:
            return False