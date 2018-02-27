import uuid
from itsdangerous import URLSafeTimedSerializer
from odyssey import app
#from config import SECURITY_PASSWORD_SALT
from odyssey.v1.status_codes import *
from odyssey.v1.status_messages import *

def generate_id():
    return str(uuid.uuid4())

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

def send_mail(sender, receiver, name=None, subject=None, text=None, html=None, reply_to=None, bcc=None, files=None,
              file_names=None, img_files=None, img_file_names=None, cc=None):
    """
    Sends mail asynchronously.
    :param sender: Sender mail.
    :param receiver: Receiver mail.
    :param name: Name of sender.
    :param subject: Subject of mail.
    :param text: Text version of mail.
    :param html: HTML version of mail.
    :param reply_to: Reply to.
    :param bcc: Blind carbon copy.
    :param files: list of files to be attached.
    :param file_names: File names from the attached list
    :return: None
    """
    import os
    from flask import Flask
    from flask_mail import Mail,Message
    from email.mime.image import MIMEImage
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication
    import smtplib
    from config import MAIL_SERVER
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    LOGIN_USER_NAME = app.config['MAIL_USERNAME']
    LOGIN_PASSWD = app.config['MAIL_PASSWORD']
    SMTP_SERVER = MAIL_SERVER
    try:
        message = MIMEMultipart('alternative')
        message['From'] = '{}<{}>'.format(name, sender)
        message['To'] = ",".join(receiver)
        if cc:
            message['CC'] = ",".join(cc)
        message['Subject'] = subject
        if reply_to:
            message.add_header('reply-to', reply_to)
        all_receivers = list()
        all_receivers += receiver
        if bcc:
            all_receivers += bcc
        if cc:
            all_receivers += cc
        # if bcc:
        #     message.add_header('Bcc', bcc)
        #     # receiver.append(bcc)
        if text:
            text_part = MIMEText(text, 'plain')
            message.attach(text_part)
        if html:
            html_part = MIMEText(html, 'html')
            message.attach(html_part)
        for index, f in enumerate(files or []):
            part = MIMEApplication(
                f.read(),
                Name=file_names[index]
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % file_names[index]
            message.attach(part)
        for index, f in enumerate(img_files or []):
            part = MIMEImage(
                f.read(),
                name=img_file_names[index]
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % img_file_names[index]
            message.attach(part)
        connection = smtplib.SMTP_SSL(host=SMTP_SERVER,port=465)
        connection.ehlo()
        #connection.starttls()
        connection.set_debuglevel(True)
        connection.login(LOGIN_USER_NAME, LOGIN_PASSWD)
        try:
            connection.sendmail(sender, all_receivers, message.as_string())
            print "SMTP mail sent:"
        finally:
            connection.quit()
    except Exception, ex:
        import traceback
        print traceback.print_exc()
        print "Mail Sending Failed: %s" % str(ex)

def unauthorized_view():
    from flask import jsonify

    response = jsonify(
        status=UNAUTHORIZED,
        message=UNAUTHORIZED_VIEW
    )
    response.status_code = UNAUTHORIZED
    return response


# def generate_random_code(length=6):
#     """
#     Generates a N digit random code.
#     :param length: Random code which need to be generated.
#     :return: random number of N digits.
#     """
#     range_start = 10 ** (length - 1)
#     range_end = (10 ** length) - 1
#     return randint(range_start, range_end)
#
#
# def generate_auth_token(data, expiration=6000):
#     """
#     generates an auth token from the SECRET_KEY with the given data and expiration time.
#     :param data: data to be added in token.
#     :param expiration: expiration time in seconds.
#     :return: generated token
#     """
#     serializer = Serializer(app.config.get('SECRET_KEY'), expires_in=expiration)
#     return serializer.dumps({
#         'data': data
#     })
#
#
# def verify_auth_token(token):
#     """
#     Verifies the auth token from the SECRET_KEY
#     :param token:
#     :return:
#     """
#     serializer = Serializer(app.config.get('SECRET_KEY'))
#     try:
#         data, header = serializer.loads(token, return_header=True)
#         return data
#     except BadSignature:
#         return None
#     except SignatureExpired:
#         return None
#
# @celery.task(bind=True)
# def send_sms(self, phone, message):
#     from odyssey import sentry
#     try:
#         with app.app_context():
#             send_sms_to_phone(phone, message)
#     except:
#         app.logger.error("Error sending sms : phone : {}".format(phone))
#         sentry.captureException()
#
# def send_sms_to_phone(phone, message):
#     """
#     send sms to phone.
#     :param phone: phone number to which to send the code. Should be in E164 format without a "+".
#     :param message: message to be sent.
#     :return: plivo response message with status code.
#     """
#     p = plivo.RestAPI(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN)
#     params = {
#         'src': PLIVO_PHONE_NUMBER,  # Sender's phone number with country code
#         'dst': phone,  # Receiver's phone Number with country code
#         'text': message,  # Your SMS Text Message - English
#         'url': "http://example.com/report/",  # The URL to which with the status of the message is sent
#         'method': 'POST'  # The method used to call the url
#     }
#     return p.send_message(params)
#
#
# def send_call_to_phone(phone, params):
#     p = plivo.RestAPI(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN)
#     return p.make_call(params)
#
#
# def write_to_s3(phone, code):
#     phone = phone.strip('+')
#     welcome = "Dear user. "
#     message = "Your verification code is " + convert_number_to_text(code)
#     speaking_text = {
#         "Response": {
#             "Speak": welcome + message + ". " + message + ". " + message + ". "
#         }
#     }
#     xml_data = xmltodict.unparse(speaking_text, pretty=True)
#     s3 = boto3.resource('s3')
#     file_name = str(phone) + ".xml"
#     s3.Bucket('com..verification').put_object(Key=file_name, Body=xml_data, ContentType='text/xml')
#
#
# def convert_number_to_text(number):
#     number_code = str(number)
#     text_string = []
#     for i in range(0, len(number_code)):
#         number = number_code[i]
#         text_string.append(NUM_TO_STR_DICT[number])
#
#     return ' '.join(text_string)
#

def add_default_values():
    from odyssey.v1.models.rate_type import RateType
    from odyssey.v1.models.days_type_info import DaysTypeInfo
    from odyssey.v1.models.season_master import SeasonsMaster
    from odyssey import db
    #rates = ['online','guest','Member']
    days = ['weekday','weekend','holiday','closed']
    seasons = ['Summer','Spring','Winter','Fall','Shoulder Season','Active/On Season','Inactive/Off Season']

    # for rate in rates:
    #     obj = RateType(
    #         id = generate_id(),
    #         name=rate
    #     )
    #     db.session.add(obj)
    for day in days:
        obj = DaysTypeInfo(
            id = generate_id(),
            day_type=day
        )
        db.session.add(obj)
    for season in seasons:
        obj = SeasonsMaster(
            id= generate_id(),
            name=season
        )
        db.session.add(obj)

    db.session.commit()
    app.logger.info("Successfully added default values")

def get_default_values():
    from odyssey.v1.models.rate_type import RateType
    from odyssey.v1.models.days_type_info import DaysTypeInfo
    from odyssey.v1.models.season_master import SeasonsMaster
    result = dict()
    seasons = SeasonsMaster.query.all()
    result['seasons'] = list()
    for season in seasons:
        result['seasons'].append(season.season_serialize)
    days = DaysTypeInfo.query.all()
    result['days'] = list()
    for day in days:
        result['days'].append(day.serialize)
    return result

def upload_image_to_s3(image):
    from odyssey.v1.common.helpers import UploadToS3Helper
    picture = image.get('image')
    if picture:
        bucket_name = app.config.get('AWS_BUCKET_URL')
        app.logger.info("upload_image: bucket_name {}".format(bucket_name))
        upload_helper = UploadToS3Helper(bucket_name)
        picture_id = str(generate_id())
        app.logger.info("IMAGE: id: {} : content_type :{}".format(picture_id, picture.content_type ))
        url = upload_helper.upload('{}_{}'.format(picture_id, picture.filename), picture.read(), picture.content_type)
        return url


