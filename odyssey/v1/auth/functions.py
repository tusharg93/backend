import datetime
from pytz import timezone
import phonenumbers
from flask import request, session, render_template
from odyssey import db, login_manager_v1 as login_manager, app
from odyssey.v1.auth.exceptions import *
from odyssey.v1.models.golf_course_master import GolfCourseMaster
from odyssey.v1.models.vendor_master import VendorMaster
from odyssey.v1.common.functions import generate_id

@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user for flask login.
    :param user_id: ID of the user.
    :return: The user object
    """
    return get_member(user_id)

def get_member(login_id):
    return GolfCourseMaster.query.filter(
            GolfCourseMaster.email == login_id,
            GolfCourseMaster.is_deleted == False

    ).first()

def get_vendor(login_id):
    vendor = VendorMaster.query.filter(VendorMaster.email == login_id, VendorMaster.is_deleted == False).first()
    if vendor:
        return vendor
    return None

def process_auth(auth_function):
    if auth_function.lower() == "login":
        return user_login(request.form)
    elif auth_function.lower() == "logout":
        if session.get('user_id'):
            source = request.form.get("source",None)
            user_logout(session.get('user_id'),source)


def user_login(member_data):

    login_id = member_data.get('login_id')
    password = member_data.get('password')
    source = member_data.get('source',None)
    if not (login_id and password):
        raise BadRequestException
    if not source or source == "golf_course":
        member = get_member(login_id)
    else:
        member = get_vendor(login_id)
    if not member:
        app.logger.info('[Login not found login id {}]'.format(login_id))
        raise UserNotFoundException
    if not member.is_email_verified:
        raise EmailNotVerifiedException
    if member.verify_password(password=password):
        flag  = True
        if not member.activated_on:
            member.activated_on = datetime.datetime.now(timezone('UTC'))
            db.session.add(member)
            db.session.commit()
            flag = False
        # if not source or source == "golf_course":
        #     create_session_key(member.id, session.sid)
        # else:
        #     create_vendor_session_key(member.id,session.sid)
        # session['user_id'] = member.id
        return {"country": member.country if member.country else None,"activated":flag,"id":member.id,"token":member.auth_token, "source":source}
    app.logger.info('[Login Incorrect : Login {} ]'.format(login_id))
    raise UserWrongPasswordException

# def login_check(member_id,source):
#
#     check_in_login = LoginTokens.query.filter(LoginTokens.member_id == member_id,
#                                               LoginTokens.source == source).first()
#     if check_in_login:
#         blacklist = BlacklistToken(token=check_in_login.short_token)
#         db.session.add(blacklist)
#         db.session.delete(check_in_login)
#         db.session.commit()

def create_vendor_session_key(member_id, session_id):
    from odyssey.v1.models.member_session_keys import MemberSessionKeys
    if not MemberSessionKeys.query.filter(MemberSessionKeys.session_id == session_id).count():
        member_session_key = MemberSessionKeys(
            uuid=generate_id(),
            member_id=member_id,
            session_id=session_id,
        )
        db.session.add(member_session_key)
        db.session.commit()

def create_session_key(member_id, session_id):
    from odyssey.v1.models.member_session_keys import MemberSessionKeys
    if not MemberSessionKeys.query.filter(MemberSessionKeys.session_id == session_id).count():
        member_session_key = MemberSessionKeys(
            uuid=generate_id(),
            member_id=member_id,
            session_id=session_id,
        )
        db.session.add(member_session_key)
        db.session.commit()


def user_logout(member_id, source = None):
    from odyssey.v1.models.member_session_keys import MemberSessionKeys
    from odyssey.v1.models.vendor_session_keys import VendorSessionKeys
    from odyssey.v1.models.login_sessions import LoginSessions
    if member_id and (not source or source == "golf_course"):
        MemberSessionKeys.query.filter(
            MemberSessionKeys.session_id == session.sid,
            MemberSessionKeys.member_id == member_id
        ).delete()
    else:
        VendorSessionKeys.query.filter(
            VendorSessionKeys.session_id == session.sid,
            VendorSessionKeys.member_id == member_id
        ).delete()
        LoginSessions.query.filter(
            LoginSessions.session_id == '{}:{}'.format(
                app.config.get('SESSION_KEY_PREFIX') or 'session',
                session.sid
            )
        ).delete()
        if 'user_id' in session:
            del session['user_id']
        db.session.commit()

#
# @celery.task
# def clear_cookies():
#     from odyssey.v2.auth.models.member_session_keys import MemberSessionKeys
#     from odyssey.v2.auth.models.login_sessions import LoginSessions
#     try:
#         LoginSessions.query.filter(~LoginSessions.session_id.in_(
#             ["{}:{}".format('session', x.session_id) for x in MemberSessionKeys.query.all()]
#         )).delete(synchronize_session=False)
#         db.session.expire_all()
#     except:
#         db.session.rollback()
#         app.logger.error("Error in clear_cookies")

def get_current_user():
    id = request.headers.get('id')
    token = request.headers.get('token')
    source = request.headers.get('source')
    if id and token:
        if not source or source == "golf_course":
            return GolfCourseMaster.query.filter(GolfCourseMaster.id == id,GolfCourseMaster.auth_token == token).first()
        else:
            return VendorMaster.query.filter(VendorMaster.id == id, VendorMaster.auth_token == token).first()
    return None
#
# def dashboard_logout():
#
#     auth_header = request.headers.get('Authorization')
#     if auth_header:
#         auth_token = auth_header.split(" ")[1]
#     else:
#         auth_token = ''
#     if auth_token:
#         login_token = LoginTokens.query.filter(LoginTokens.short_token == auth_token, LoginTokens.source == "mobile_dashboard").first()
#         if login_token:
#             # mark the token as blacklisted
#             blacklist_token = BlacklistToken(token=auth_token)
#             db.session.add(blacklist_token)
#             db.session.commit()


# def get_otp(login_id):
#     member = get_member(login_id)
#     if not member:
#         raise UserNotFoundException
#     otp = generate_random_code(length=6)
#     auth_token = generate_auth_token(data={
#         'login_id': login_id,
#         'otp': otp
#     })
#     number = phonenumbers.phonenumber.PhoneNumber()
#     number.country_code = member.country_code
#     number.national_number = member.mobile
#     send_otp_mobile(str(phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)), otp)
#     send_otp_mail(member.email, otp)
#     return auth_token
#
#
# def get_otp_call(login_id, auth_token):
#     member = get_member(login_id)
#     if not member:
#         raise UserNotFoundException
#     data = verify_auth_token(auth_token)
#     if not data:
#         raise WrongAuthTokenException
#     data = data['data']
#     if data.get('login_id') == login_id:
#         send_otp_call(phone='91' if not member.country_code else member.country_code + member.mobile,
#                       otp=data.get('otp'))
#         return None
#     raise WrongAuthTokenException
#
#
# def send_otp_mobile(mobile, otp):
#     if mobile:
#         messsage = '{} is your One Time Password for Loktra.'.format(otp)
#         mobile = mobile.strip('+')
#         send_sms_to_phone(phone=mobile, message=messsage)
#
#
# def send_otp_call(phone, otp):
#     amazon_s3_verification_url = app.config['AMAZON_S3_VERIFICATION_CODE_URL']
#     from config import PLIVO_PHONE_NUMBER
#     phone = phone.strip('+')
#     write_to_s3(phone=phone, code=otp)
#     params = {
#         'to': phone,
#         'from': PLIVO_PHONE_NUMBER,
#         'answer_url': amazon_s3_verification_url + str(phone) + ".xml",
#         'answer_method': "GET",
#     }
#     print phone, " ", params
#     send_call_to_phone(phone=phone, params=params)
#
#
# def send_otp_mail(email, otp):
#     if email:
#         send_mail(
#             sender=LOKTRA_MAIL,
#             receiver=[email],
#             name="Loktra Team",
#             subject="Verification Code for Loktra: {}".format(otp),
#             text="Reset your password with the following code. Thank you for signing up with Loktra.",
#             html=render_template('verify_reset_password_otp.html', otp=otp)
#         )
#
#
# def validate_otp(login_id, otp, auth_token):
#     if not login_id:
#         raise OTPLoginIDNullException
#     if not otp:
#         raise OTPSelfNullException
#     if not auth_token:
#         raise OTPAuthTokenNullException
#     data = verify_auth_token(auth_token)
#     if not data:
#         raise WrongAuthTokenException
#     data = data['data']
#     if data.get('login_id') == login_id and str(data.get('otp')) == str(otp):
#         auth_token = generate_auth_token(data={
#             'login_id': login_id,
#             'validated': True
#         })
#         return auth_token
#     raise WrongOTPException
#
#
# def reset_password(login_id, new_password, auth_token):
#     from odyssey.v2.members.mis_context_based_update import update_mis_member_data, BASIC_CONTEXT
#
#     if not login_id:
#         raise OTPLoginIDNullException
#     if not new_password:
#         raise ResetPasswordNullException
#     if not auth_token:
#         raise OTPAuthTokenNullException
#     data = verify_auth_token(auth_token)
#     if not data:
#         raise WrongAuthTokenException
#     data = data['data']
#     if data.get('login_id') == login_id and data.get('validated') is True:
#         first_login = False
#         member = get_member(login_id)
#         member.hash_password(new_password)
#         if not member.activated_on:
#             member.activated_on = datetime.datetime.utcnow()
#             first_login = True
#         db.session.commit()
#         update_mis_member_data(member_id=member.id, context_list=[BASIC_CONTEXT])
#         if first_login:
#             app.logger.info("first login crons triggered : member_id: {}".format(member.id))
#             from odyssey.v2.common.cron_trigger_functions import trigger_reporting_structure_crons
#             trigger_reporting_structure_crons()
#         source = request.args.get('source') or request.form.get('source') or "agent_app"
#         member_data = {
#             'login_id': login_id,
#             'password': new_password,
#             'source': source
#         }
#         return user_login(member_data=member_data)
#     raise BadRequestException
#
#
# def get_organization_details():
#     organization_profile = OrganizationProfile.query.first()
#     if not organization_profile:
#         raise OrganizationNotFoundException
#     return organization_profile