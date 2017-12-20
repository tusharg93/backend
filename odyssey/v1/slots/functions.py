from odyssey import db, app
from datetime import datetime, timedelta
from odyssey.v1.models.gc_special_days_info import GCSpecialDaysInfo
from odyssey.v1.models.gc_rates_info import GCRatesInfo
from odyssey.v1.models.days_type_info import DaysTypeInfo
from odyssey.v1.models.gc_seasons_info import GCSeasonsInfo
from odyssey.v1.models.rate_type import RateType
from odyssey.v1.models.golf_course_master import GolfCourseMaster
from odyssey.v1.models.dynamic_tables import *
from odyssey.v1.common.functions import generate_id
from sqlalchemy import func
#id,time,date,day_type,season_id,price_1,price_2,status,min_golfers,

def slot_generator(gc_id):
    gc_info =  db.session.query(GolfCourseMaster.id,GolfCourseMaster.duration_live_slots,GolfCourseMaster.weekends,GolfCourseMaster.weekdays).filter(GolfCourseMaster.id == gc_id).first()
    today = datetime.today()
    year_end = today.replace(day=31, month=12)
    diff = (year_end - today).days
    generate_slots(gc_info, today)
    if diff < (gc_info.duration_live_slots * 30):
        next_year_end = year_end.replace(year=today.year + 1)
        generate_slots(gc_info, next_year_end)

def generate_slots(gc_object, today):
    gc_id = gc_object.id
    table_object   = get_gc_slot_table_object("gc_{}_slots".format(gc_id))
    if table_object is None:
        create_gc_slot_table(gc_id)
        table_object = get_gc_slot_table_object("gc_{}_slots".format(gc_id))
    gc_seasons_obj = GCSeasonsInfo.query.filter(GCSeasonsInfo.gc_id == gc_id).all()
    weekdays = gc_object.weekdays.split(',')
    weekends = gc_object.weekends.split(',')
    days_type = DaysTypeInfo.query.filter(DaysTypeInfo.day_type.in_(['weekday','weekend'])).order_by(DaysTypeInfo.day_type).all()
    weekday_id = days_type[0].id
    weekend_id = days_type[0].id
    current_year = today.year
    for gc_season_details in gc_seasons_obj:
        start_date = gc_season_details.start_date
        end_date = gc_season_details.end_date
        season_id = gc_season_details.season_id
        if not start_date or not end_date:
            app.logger.info("Season {} duration not defined".format(season_id))
            continue
        start_date = start_date.replace(year=current_year)
        end_date = end_date.replace(year=current_year)
        if start_date < today:
            start_date = today
        if end_date < today:
            end_date = today
        if start_date == end_date:
            app.logger.info("This season has passed {}".format(season_id))
            continue
        start_time = gc_season_details.start_time
        end_time = gc_season_details.end_time
        if not start_time or not end_time:
            app.logger.info("No tee times defined for this season {}".format(season_id))
            continue
        interval = gc_season_details.tee_interval
        if not interval:
            app.logger.info("Interval not defined for this season {}".format(season_id))
            continue
        insert_data = list()
        online_rate_id = RateType.query.filter(RateType.name == 'online').first().id
        rates_info = GCRatesInfo.query.filter(GCRatesInfo.gc_id == gc_id,
                                              GCRatesInfo.season_id == season_id,
                                              GCRatesInfo.rate_type == online_rate_id).all()
        wk_9_price = None
        wk_18_price = None
        we_9_price = None
        we_18_price = None
        for rates in rates_info:
            if rates.day_type == weekday_id:
                wk_9_price = rates.hole_9_price
                wk_18_price = rates.hole_18_price
            else:
                we_9_price = rates.hole_9_price
                we_18_price = rates.hole_18_price
        while start_date <= end_date:
                current_start = datetime.combine(start_date,start_time)
                current_end = datetime.combine(start_date,end_time)
                day_id = weekday_id if current_start.strftime('%a') in weekdays else weekend_id
                while current_start <= current_end:
                    d = dict()
                    d['id'] = generate_id()
                    d['date'] = start_date
                    d['tee_time'] = datetime.strptime('{}:{}'.format(current_start.hour,current_start.minute),'%H:%M').time()
                    d['season_id'] = season_id
                    d['day_type'] = day_id
                    d['hole_9_price'] = wk_9_price if day_id == weekday_id else we_9_price
                    d['hole_18_price'] = wk_18_price if day_id == weekday_id else we_18_price
                    d['min_golfers'] = 4
                    d['slot_status'] = 'OPEN'
                    insert_data.append(d)
                    current_start = current_start + timedelta(minutes=interval)
                start_date = start_date + timedelta(days=1)
        try:
            if len(insert_data) > 0:
                db.session.execute(table_object.insert(), insert_data, bind=db.get_engine(app, 'base_db'))
        except:
            import traceback
            app.logger.error(traceback.print_exc())
    app.logger.info("Successfully created slots for gc_id {}".format(gc_id))


def get_week_type_slots(gc_id, season_id, day_type):

    table = get_gc_slot_table_object("gc_{}_slots".format(gc_id))
    if not table:
        app.logger.error("Table doesnt exist")
        return None
    day_type_id = DaysTypeInfo.query.filter(DaysTypeInfo.name == day_type).first().id
    next_date = (datetime.today() + timedelta(days=1)).date()
    gc_season_info = db.session.query(GCSeasonsInfo.start_time,GCSeasonsInfo.end_time).filter(
        GCSeasonsInfo.gc_id == gc_id,
        GCSeasonsInfo.season_id == season_id
    ).first()
    total_week_type_slots = db.session.query(table.c.date,func.count('*').label('slots_count')).filter(table.c.season_id == season_id,
                                                         table.c.day_type == day_type_id,
                                                         table.c.date >= next_date
                                                         ).group_by(table.c.date).limit(1)
    week_type_slots = db.session.query(table).filter(table.c.season_id == season_id,
                                                   table.c.day_type == day_type_id,
                                                   table.c.tee_time >= gc_season_info.start_time,
                                                   table.c.tee_time <= gc_season_info.end_time).order_by(table.c.date).limit(int(total_week_type_slots.slots_count))
    result = list()
    for slot in week_type_slots:
        d = dict()
        d['tee_time'] = slot.tee_time.strftime('%H:%M')
        d['hole_9_price'] = slot.hole_9_price
        d['hole_18_price'] = slot.hole_18_price
        result.append(d)
    return result


def update_week_type_slots(gc_id, json_data):
    day_type = json_data.get('day_type')
    season_id = json_data.get('season_id')
    slots = json_data.get('slots')
    table =  get_gc_slot_table_object("gc_{}_slots".format(gc_id))
    for slot in slots:
        tee_time = slot.get('tee_time')
        hole_9_price = slot.get('hole_9_price')
        hole_18_price = slot.get('hole_18_price')
        slot_status = slot.get('slot_status',None)
        if not slot_status:
            slot_status = 'OPEN'
        #tee_slots = db.session.query(table).filter(table.c.tee_time == tee_time,
        #                                           table.c.season_id == season_id,
        #                                           table.c.day_type == day_type).all()
        db.session.execute(
            "update \"gc_{}_slots\" set hole_9_price = {}, hole_18_price = {} , slot_status = '{}' where tee_time = '{}' and season_id = '{}' and day_type = '{}';"
                .format(gc_id, hole_9_price, hole_18_price, slot_status, tee_time, season_id, day_type),
            bind=db.get_engine(app, 'base_db'))
        db.session.commit()
