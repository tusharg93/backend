from odyssey import app, db
from odyssey.v1.common.functions import generate_id
from flask import render_template
from odyssey.v1.common.constants import SERVER_IP
from odyssey.v1.common.functions import send_mail, generate_confirmation_token, confirm_token

def register_vendor_data(form_data):
    from odyssey.v1.models.vendor_master import VendorMaster
    name = form_data.get('name', None)
    country = form_data.get('country', None)
    city = form_data.get('city', None)
    mobile = form_data.get('mobile', None)
    country_code = form_data.get('country_code', None)
    email = form_data.get('email', None)
    password = form_data.get('password', None)
    website_url = form_data.get('website_url',None)
    # if get_member(email):
    #     raise UserExistsException
    MAIL_USERNAME = app.config.get('MAIL_USERNAME')
    vendor_object = VendorMaster(
        id=generate_id(),
        name=name,
        country=country,
        city=city,
        mobile=mobile,
        country_code=country_code,
        website_url= website_url,
        email=email,
        password=password
    )
    token = vendor_object.get_auth_token()
    vendor_object.auth_token = token
    # if not official_email:
    #     gc_object.official_email = False
    # else:
    #     gc_object.official_email = True
    db.session.add(vendor_object)
    db.session.commit()
    token = generate_confirmation_token(email=email)
    verify_url = 'http://{}/verify/{}?type=vendor'.format(SERVER_IP, token)
    with app.app_context():
        html_data = render_template("email_confirmation.html", confirm_url=verify_url)
    send_mail(
        sender=MAIL_USERNAME,
        receiver=[email],
        bcc=[MAIL_USERNAME],
        name="TeeTimes Team",
        subject="TeeTimes Registration Successful !",
        html=html_data,
    )

def create_vendor_profile(json_data, vendor_id):
    from odyssey.v1.models.vendor_master import VendorMaster
    v_object = VendorMaster.query.get(vendor_id)
    description = json_data.get('about', None)
    contact_name = json_data.get('contact_name', None)
    designation = json_data.get('designation', None)
    contact_mobile = json_data.get('contact_mobile', None)
    address_1 = json_data.get('address_line_1', None)
    address_2 = json_data.get('address_line_2', None)
    weekday_hrs = json_data.get('weekday_hrs', None)
    weekday_start_time = weekday_hrs.get('start_time', None)
    weekday_end_time = weekday_hrs.get('end_time', None)
    if weekday_start_time and weekday_end_time:
        weekday_hrs_string = weekday_start_time + " to " + weekday_end_time
    else:
        weekday_hrs_string = None
    weekend_hrs = json_data.get('weekday_hrs', None)
    weekend_start_time = weekend_hrs.get('start_time', None)
    weekend_end_time = weekend_hrs.get('end_time', None)
    if weekend_start_time and weekend_end_time:
        weekend_hrs_string = weekend_start_time + " to " + weekend_end_time
    else:
        weekend_hrs_string = None
    facebook_url = json_data.get('fb_url',None)
    twitter_url = json_data.get('twitter_url',None)
    insta_url = json_data.get('insta_url',None)
    linkedin_url = json_data.get('linkedin_url',None)
    gplus_url = json_data.get('gplus_url')
    v_object.description = description
    v_object.contact_name = contact_name
    v_object.contact_mobile = contact_mobile
    v_object.designation = designation
    v_object.address_1 = address_1
    v_object.address_2 = address_2
    v_object.weekday_hrs = weekday_hrs_string
    v_object.weekend_hrs = weekend_hrs_string
    v_object.facebook_url = facebook_url
    v_object.twitter_url = twitter_url
    v_object.insta_url = insta_url
    v_object.linkedin_url = linkedin_url
    v_object.gplus_url = gplus_url
    db.session.add(v_object)
    db.session.commit()
