from odyssey.v1.models.golf_course_master import GolfCourseMaster
from odyssey.v1.common.functions import generate_id
from odyssey.v1.models.dynamic_tables import create_gc_slot_table
from odyssey import db, app
import datetime
from flask import render_template
from odyssey.v1.common.constants import SERVER_IP
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
    MAIL_USERNAME = app.config.get('MAIL_USERNAME')
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
    # if not official_email:
    #     gc_object.official_email = False
    # else:
    #     gc_object.official_email = True
    db.session.add(gc_object)
    db.session.commit()
    create_gc_slot_table(gc_object.id)
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
    if email:
        user    =   GolfCourseMaster.query.filter(GolfCourseMaster.email == email).first()
        if user:
            user.is_email_verified = True
            user.confirmed_on = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            return True
    return False

def gc_fill_section_1(json_data, gc_id):
    from odyssey.v1.models.golf_course_master import GolfCourseMaster
    is_9_hole = json_data.get('hole_9', None)
    is_18_hole = json_data.get('hole_18', None)
    tee_avl = json_data.get('tee_avl',None)
    currency = json_data.get('currency', None)
    time_zone = json_data.get('timezone',None)
    member_flag = json_data.get('member', None)
    guest_flag = json_data.get('guest', None)
    online_flag = json_data.get('online', None)
    live_slots_duration = json_data.get('duration', None)
    gc_details = GolfCourseMaster.query.filter(GolfCourseMaster.id == gc_id).first()
    if gc_details:
        gc_details.hole_9_flag = True if is_9_hole else False
        gc_details.hole_18_flag=True if is_18_hole else False
        gc_details.tee_avl = tee_avl
        gc_details.time_zone = time_zone
        gc_details.currency = currency
        gc_details.is_guest = True if guest_flag else False
        gc_details.is_member=True if member_flag else False
        gc_details.is_online=True if online_flag else False
        gc_details.duration=int(live_slots_duration) if live_slots_duration else 3
        db.session.add(gc_details)
        db.session.commit()

def gc_fill__section_2(json_data, gc_id):
    from odyssey.v1.models.gc_special_days_info import GCSpecialDaysInfo
    gc_object = GolfCourseMaster.query.filter(GolfCourseMaster.id == gc_id).first()
    if gc_object:
        weekdays = json_data.get('weekdays')
        weekends = json_data.get('weekends')
        gc_object.weekdays = ','.join(weekdays)
        gc_object.weekends = ','.join(weekends)
        db.session.add(gc_object)
        closed_info = json_data.get('closed')
        for close in closed_info:
            day = close.get('day')
            day_type = close.get('day_type')
            full_day = close.get('full_day')
            special_day_obj = GCSpecialDaysInfo(
                id=generate_id(),
                gc_id=gc_id,
                day_type=day_type,
                day=day
            )
            if not full_day:
                special_day_obj.full_day   =    False
            db.session.add(special_day_obj)
        db.session.commit()

def gc_fill_section_3(json_data, gc_id):
    from odyssey.v1.models.season_master import SeasonsMaster
    from odyssey.v1.models.gc_seasons_info import GCSeasonsInfo
    seasons = json_data.get('seasons')
    for season in seasons:
        season_id = season.get('id',None)
        season_name = season.get('name',None)
        season_start = season.get('start_date',None)
        season_end = season.get('end_date',None)
        season_type = season.get('type',None)
        if season_type:
            new_season = SeasonsMaster(
                id=season_id,
                name=season_name
            )
            db.session.add(new_season)
            db.session.commit()
        season_start = datetime.datetime.strptime(season_start,"%m-%d").date()
        season_end   = datetime.datetime.strptime(season_end,"%m-%d").date()
        gc_season_obj = GCSeasonsInfo(
            id =  generate_id(),
            gc_id=gc_id,
            season_id=season_id,
            start_date=season_start,
            end_date=season_end
        )
        db.session.add(gc_season_obj)
    db.session.commit()

def gc_fill_section_4(json_data, gc_id):
    from odyssey.v1.models.gc_seasons_info import GCSeasonsInfo
    from odyssey.v1.models.gc_rates_info import GCRatesInfo
    from odyssey.v1.models.gc_special_days_info import GCSpecialDaysInfo
    import time
    seasons_info  = json_data.get('seasons_info')
    for season_data in seasons_info:
        season_id = season_data.get('id', None)
        start_time = season_data.get('start_time',None)
        end_time   = season_data.get('end_time',None)
        time_interval = season_data.get('interval',None)
        gc_season_obj = GCSeasonsInfo.query.filter(GCSeasonsInfo.gc_id == gc_id,
                                                   GCSeasonsInfo.season_id == season_id).first()
        if gc_season_obj:
            gc_season_obj.start_time = time.strptime(start_time,'%H:%M')
            gc_season_obj.end_time = time.strptime(end_time,'%H:%M')
            gc_season_obj.tee_interval = time_interval
            db.session.add(gc_season_obj)
        rates = season_data.get('rates')
        for rate in rates:
            gc_rates_obj = GCRatesInfo(
                id=generate_id(),
                season_id=season_id,
                gc_id=gc_id,
                day_type=rate.get('day_type'),
                hole_9_price=rate.get('prcie_9'),
                hole_18_price=rate.get('price_18'),
                rate_type=rate.get('rate_type'),
                price=rate.get('price')
            )
            db.session.add(gc_rates_obj)
        special_day_obj = GCSpecialDaysInfo.query.filter(
                        GCSpecialDaysInfo.gc_id == gc_id
        ).first()
        if special_day_obj and special_day_obj.full_day == False:
            maintenance = season_data.get('maintenance',None)
            if maintenance:
                stime = maintenance.get('start_time',None)
                etime = maintenance.get('end_time',None)
                if stime and etime:
                    special_day_obj.start_time = time.strptime(stime,'%H:%M')
                    special_day_obj.end_time = time.strptime(etime,'%H:%M')
                    special_day_obj.season_id = season_id
                    db.session.add(special_day_obj)

    db.session.commit()








