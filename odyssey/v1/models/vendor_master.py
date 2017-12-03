import datetime
from odyssey import db
from odyssey.v1.common.constants import VENDOR_MASTER, COUNTRIES_MASTER, CITIES_MASTER
from passlib.apps import custom_app_context as pwd_context


class VendorMaster(db.Model):
    __tablename__ = VENDOR_MASTER
    __bind_key__ = 'base_db'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    country_id = db.Column(db.String,db.ForeignKey('{}.id'.format(COUNTRIES_MASTER)))
    city_id = db.Column(db.String,db.ForeignKey('{}.id'.format(CITIES_MASTER)))
    founder = db.Column(db.String)
    established = db.Column(db.DateTime)
    logo_url = db.Column(db.String)
    website_url = db.Column(db.String)
    description = db.Column(db.String)
    pg_avl = db.Column(db.Boolean)
    regions_actv = db.Column(db.String)
    email = db.Column(db.String)
    is_email_verified = db.Column(db.Boolean,default=False)
    password = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.country_id = kwargs.get('country_id')
        self.city_id    = kwargs.get('city_id')
        self.founder = kwargs.get('founder')
        self.established = kwargs.get('established')
        self.logo_url = kwargs.get('logo_url')
        self.website_url = kwargs.get('website_url')
        self.description = kwargs.get('description')
        self.pg_avl = kwargs.get('pg_avl')
        self.regions_actv = kwargs.get('regions_actv')
        self.email = kwargs.get('email')
        self.hash_password(kwargs.get('password'))

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