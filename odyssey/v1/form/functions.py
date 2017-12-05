from odyssey.v1.models.golf_course_master import GolfCourseMaster
from odyssey.v1.common.functions import generate_id
from odyssey import db, app
import datetime
from flask import render_template
from odyssey.v1.common.constants import MAIL_USERNAME, SERVER_IP
from odyssey.v1.common.functions import send_mail, generate_confirmation_token, confirm_token
from odyssey.v1.auth.functions import get_member
from odyssey.v1.form.customer_errors import UserExistsException

def register_form_data(form_data):
    name    =   form_data.get('name',None)
    country =   form_data.get('country',None)
    city    =   form_data.get('city',None)
    mobile  =   form_data.get('mobile',None)
    country_code = form_data.get('country_code',None)
    email   =   form_data.get('email',None)
    password =  form_data.get('password',None)
    official_email = form_data.get('official_email',True)
    # if get_member(email):
    #     raise UserExistsException

    gc_object = GolfCourseMaster(
        id = generate_id(),
        name = name,
        country=country,
        city=city,
        mobile=mobile,
        country_code=country_code,
        email=email,
        password=password
    )
    if not official_email:
        gc_object.official_email = False
    else:
        gc_object.official_email = True
    db.session.add(gc_object)
    db.session.commit()
    token   =   generate_confirmation_token(email=email)
    verify_url  =   'http://{}/verify/{}'.format(SERVER_IP, token)
    with app.app_context():
        html_data = render_template("email_confirmation.html",confirm_url = verify_url)
    send_mail(
        sender=MAIL_USERNAME,
        receiver=[email],
        bcc=[MAIL_USERNAME],
        name="TeeTimes Team",
        subject="TeeTimes Registration Successful !",
        html=html_data,
    )

def verify_email(query):
    token   =   query.get('token')
    email   =   confirm_token(token=token)
    user    =   GolfCourseMaster.query.filter(GolfCourseMaster.email == email).first()
    if user:
        user.is_email_verified = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return True
    return False













