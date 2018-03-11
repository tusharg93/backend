from odyssey import app, db
from odyssey.v1.common.functions import generate_id
from flask import render_template
from odyssey.v1.common.functions import send_mail, generate_confirmation_token, confirm_token
from odyssey.v1.models.vendor_master import VendorMaster
import datetime

def register_vendor_data(form_data):
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
    IP = app.config.get('HOST_IP')
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
    vendor_object.auth_token = token[:32]
    # if not official_email:
    #     gc_object.official_email = False
    # else:
    #     gc_object.official_email = True
    db.session.add(vendor_object)
    db.session.commit()
    token = generate_confirmation_token(email=email)
    verify_url = 'http://{}:5000/verify/{}?type=vendor'.format(IP, token)
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
def image_upload(user_id, request):
    from odyssey.v1.common.functions import upload_image_to_s3
    user_object = VendorMaster.query.get(user_id)
    img_url = upload_image_to_s3(request.files)
    user_object.logo_url = img_url
    db.session.add(user_object)
    db.session.commit()
    return img_url

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
        weekday_start_time = datetime.datetime.strptime(weekday_start_time,"%H:%M").time()
        weekday_start_string = weekday_start_time.strftime('%I') + ':' + weekday_start_time.strftime('%M')  + weekday_start_time.strftime('%p')
        weekday_end_time = datetime.datetime.strptime(weekday_end_time, "%H:%M").time()
        weekday_end_string = weekday_end_time.strftime('%I') + ':' + weekday_end_time.strftime(
            '%M') + weekday_end_time.strftime('%p')
        weekday_hrs_string = weekday_start_string + " to " + weekday_end_string
    else:
        weekday_hrs_string  = None
    weekend_hrs = json_data.get('weekday_hrs', None)
    weekend_start_time = weekend_hrs.get('start_time', None)
    weekend_end_time = weekend_hrs.get('end_time', None)
    if weekend_start_time and weekend_end_time:
        weekend_start_time = datetime.datetime.strptime(weekend_start_time, "%H:%M").time()
        weekend_start_string = weekend_start_time.strftime('%I') + ':' + weekend_start_time.strftime(
            '%M') + weekend_start_time.strftime('%p')
        weekend_end_time = datetime.datetime.strptime(weekend_end_time, "%H:%M").time()
        weekend_end_string = weekend_end_time.strftime('%I') + ':' + weekend_end_time.strftime(
            '%M') + weekend_end_time.strftime('%p')
        weekend_hrs_string = weekend_start_string + " to " + weekend_end_string
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

def manage_course_section(vendor_id):
    try:
        from odyssey.v1.models.golf_course_master import GolfCourseMaster
        from odyssey.v1.models.vendor_course_contract import VendorCourseContract
        result = dict()
        result['pending']  =  list()
        result['accepted'] = list()
        result['declined'] = list()
        result['all']     = list()
        contract = VendorCourseContract.query.filter(VendorCourseContract.v_id == vendor_id).all()
        contract_ids = list()
        if contract:
            for relation in contract:
                d = dict()
                contract_ids.append(relation.gc_id)
                gc_object = GolfCourseMaster.query.get(relation.gc_id)
                d['id'] = relation.id
                d['gc_id'] = relation.gc_id
                d['status'] = relation.final_status
                d['requestor_status'] = relation.requestor_status
                d['request_by'] = relation.request_by
                d['gc_name'] = gc_object.name
                d['logo_url'] = gc_object.logo_url
                result[d['status'].lower()].append(d)
        if len(contract_ids) > 0:
            course_data = GolfCourseMaster.query.filter(~GolfCourseMaster.id.in_(contract_ids)).all()
        else:
            course_data = GolfCourseMaster.query.all()
        if course_data:
            result['all'] = [x.contract_serialize for x in course_data]
        return result
    except:
        import traceback
        app.logger.info("error in fetching vendor data in gc dashboard")
        app.logger.error(traceback.print_exc())
        db.session.rollback()
        return dict()

def load_home_page_data(vendor_id):
    result = dict()
    v_object = VendorMaster.query.get(vendor_id)
    if not v_object:
        return result
    result['basic_info'] = dict()
    result['basic_info'] = v_object.dashboard_serialize
    result['manage_course'] = dict()
    result['manage_course'] = manage_course_section(vendor_id)
    return result

def course_request(vendor_id, json_data):
    from odyssey.v1.models.vendor_course_contract import VendorCourseContract
    relation_id = json_data.get('id',None)
    gc_id = json_data.get('gc_id',None)
    request_status = json_data.get('status')
    if not gc_id:
        return
    if not relation_id:
        contract = VendorCourseContract(
            id=generate_id(),
            v_id=vendor_id,
            gc_id=gc_id,
            request_by=vendor_id,
            requestor_status=request_status,
            final_status='PENDING'
        )
        db.session.add(contract)
    else:
        contract = VendorCourseContract.query.get(relation_id)
        contract.final_status = request_status
    db.session.commit()