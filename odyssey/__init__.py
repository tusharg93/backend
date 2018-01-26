import os

from flask import Flask
from flask_compress import Compress
from flask_cors import CORS
from flask_login import LoginManager
from flask_redis import FlaskRedis
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from urlparse import urlparse


app = Flask(
    __name__,
    template_folder=os.path.join(os.getcwd(), 'templates'),
    static_url_path=os.path.join(os.getcwd(), 'static'),
)

app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app=app)
app.config['SESSION_SQLALCHEMY'] = db


from odyssey.v1.models.golf_course_master import GolfCourseMaster
from odyssey.v1.models.days_type_info import DaysTypeInfo
from odyssey.v1.models.rate_type import RateType
from odyssey.v1.models.gc_seasons_info import GCSeasonsInfo
from odyssey.v1.models.gc_rates_info import GCRatesInfo
from odyssey.v1.models.gc_special_days_info import GCSpecialDaysInfo
#from odyssey.v1.models.login_sessions import LoginSessions
from odyssey.v1.models.slots_master import SlotsMaster
from odyssey.v1.models.member_session_keys import MemberSessionKeys
# from odyssey.v1.models.course_facilities_master import CourseFacilitiesMaster
# from odyssey.v1.models.rate_inclusions_master import RateInclusionsMaster
# from odyssey.v1.models.course_images_master import CourseImageMaster
# from odyssey.v1.models.regions_master import RegionsMaster
# from odyssey.v1.models.vendor_master import VendorMaster
# from odyssey.v1.models.slots_master import SlotsMaster
from odyssey.v1.models.season_master import SeasonsMaster
# from odyssey.v1.models.status_master import StatusMaster


db.create_all()
db.session.commit()
Session(app)
login_manager_v1 = LoginManager(app)
compress = Compress(app)
CORS(app, supports_credentials=True)
