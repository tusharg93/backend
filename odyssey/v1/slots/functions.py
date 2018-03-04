from odyssey import db, app
from datetime import datetime, timedelta
from odyssey.v1.models.gc_rates_info import GCRatesInfo
from odyssey.v1.models.days_type_info import DaysTypeInfo
from odyssey.v1.models.gc_seasons_info import GCSeasonsInfo
from odyssey.v1.models.golf_course_master import GolfCourseMaster
from odyssey.v1.models.dynamic_tables import *
from odyssey.v1.common.functions import generate_id
from sqlalchemy import func

def slot_generator(gc_id):
    gc_info =  db.session.query(GolfCourseMaster.id,GolfCourseMaster.duration_live_slots,GolfCourseMaster.weekends,GolfCourseMaster.weekdays, GolfCourseMaster.time_zone, GolfCourseMaster.min_weekdays, GolfCourseMaster.min_weekends, GolfCourseMaster.maintenance_day, GolfCourseMaster.maintenance_type).filter(GolfCourseMaster.id == gc_id).first()
    today = datetime.utcnow()
    year_end = today.replace(day=31, month=12,hour=18,minute=30,second=0)
    generate_slots(gc_info, today, year_end)

def generate_slots(gc_object, today, year_end):
    gc_id = gc_object.id
    print today
    today_date = today.date()
    today_year = today.year
    if gc_object.time_zone:
        t = gc_object.time_zone[1:]
        t = t.split(':')
        if gc_object.time_zone[0] == '+':
            if len(t) == 2:
                today = today + timedelta(hours=int(t[0]), minutes=int(t[1]))
            else:
                today = today + timedelta(hours=int(t[0]))
    table_object   = get_gc_slot_table_object("gc_{}_slots".format(gc_id))
    if table_object is None:
        print 'table not found hence creating'
        create_gc_slot_table(gc_id)
        table_object = get_gc_slot_table_object("gc_{}_slots".format(gc_id))
    table_class_object = get_gc_table_class_object("gc_{}_slots".format(gc_id))
    table_class_object.query.delete()
    gc_seasons_obj = GCSeasonsInfo.query.filter(GCSeasonsInfo.gc_id == gc_id).all()
    min_weekdays = gc_object.min_weekdays if gc_object.min_weekdays else 4
    min_weekends = gc_object.min_weekends if gc_object.min_weekends else 4
    weekdays = gc_object.weekdays.split(',')
    weekends = gc_object.weekends.split(',')
    days_type = DaysTypeInfo.query.filter(DaysTypeInfo.day_type.in_(['weekday','weekend'])).order_by(DaysTypeInfo.day_type).all()
    weekday_id = days_type[0].id
    weekend_id = days_type[0].id
    current_year = today_year
    maintenance_day = gc_object.maintenance_day
    maintenance_type = gc_object.maintenance_type
    for gc_season_details in gc_seasons_obj:
        start_date = gc_season_details.start_date
        end_date = gc_season_details.end_date
        season_id = gc_season_details.season_id
        maintenance_stime = None
        maintenance_etime = None
        if maintenance_type == False:
            maintenance_stime = gc_season_details.maintenance_stime
            maintenance_etime = gc_season_details.maintenance_etime
        if not start_date or not end_date:
            app.logger.info("Season {} duration not defined".format(season_id))
            continue
        start_date = start_date.replace(year=current_year)
        if start_date.month > end_date.month:
            end_date = end_date.replace(year=current_year+1)
        elif start_date.month == end_date.month and start_date.day > end_date.day:
            end_date = end_date.replace(year=current_year+1)
        else:
            end_date = end_date.replace(year=current_year)

        if start_date < today_date and end_date < today_date:
            start_date = start_date.replace(year=current_year+1)
            end_date = end_date.replace(year=current_year+1)
        elif start_date <= today_date and end_date > today_date:
            start_date = today_date
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
        rates_info = GCRatesInfo.query.filter(GCRatesInfo.gc_id == gc_id,
                                              GCRatesInfo.season_id == season_id,
                                              GCRatesInfo.rate_type == 'ONLINE').all()
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
                status = 'OPEN'
                special_stime = None
                special_etime = None
                current_start = datetime.combine(start_date,start_time)
                current_end = datetime.combine(start_date,end_time)
                day_id = weekday_id if current_start.strftime('%a') in weekdays else weekend_id
                if maintenance_day and current_start.strftime('%a') == maintenance_day:
                    status = 'WEEKLY_OFF'
                    if maintenance_stime:
                        special_stime = datetime.combine(start_date, maintenance_stime)
                        special_etime = datetime.combine(start_date, maintenance_etime)
                while current_start <= current_end:
                    if current_start > today:
                        d = dict()
                        d['id'] = generate_id()
                        d['date'] = start_date
                        d['tee_time'] = datetime.strptime('{}:{}'.format(current_start.hour,current_start.minute),'%H:%M').time()
                        d['season_id'] = season_id
                        d['day_type'] = day_id
                        d['day'] = current_start.strftime("%a")
                        d['hole_9_price'] = wk_9_price if day_id == weekday_id else we_9_price
                        d['hole_18_price'] = wk_18_price if day_id == weekday_id else we_18_price
                        d['min_golfers'] = min_weekdays if day_id == weekday_id else min_weekends
                        if not special_stime:
                            d['slot_status'] = status
                        else:
                            if current_start >= special_stime and current_start <= special_etime:
                                d['slot_status'] = status
                            else:
                                d['slot_status'] = 'OPEN'
                        insert_data.append(d)
                    current_start = current_start + timedelta(minutes=interval)
                start_date = start_date + timedelta(days=1)
        try:
            if len(insert_data) > 0:
                print len(insert_data)
                db.session.execute(table_object.insert(), insert_data, bind=db.get_engine(app, 'base_db'))
                db.session.commit()
        except:
            import traceback
            app.logger.error(traceback.print_exc())
    app.logger.info("Successfully created slots for gc_id {}".format(gc_id))


def get_week_type_slots(gc_id, query_params):
    table = get_gc_slot_table_object("gc_{}_slots".format(gc_id))
    if not table:
        app.logger.error("Table doesnt exist")
        return list()
    season_id = query_params.get("season_id")
    day_type_id = query_params.get("day_type")
    #day_type_id = DaysTypeInfo.query.filter(DaysTypeInfo.name == day_type).first().id
    next_date = (datetime.today() + timedelta(days=1)).date()
    # gc_season_info = db.session.query(GCSeasonsInfo.start_time,GCSeasonsInfo.end_time).filter(
    #     GCSeasonsInfo.gc_id == gc_id,
    #     GCSeasonsInfo.season_id == season_id
    # ).first()
    total_week_type_slots = db.session.query(table.c.date.label('date'),func.count('*').label('slots_count')).filter(table.c.season_id == season_id,
                                                         table.c.day_type == day_type_id,
                                                         table.c.date >= next_date
                                                         ).group_by(table.c.date).first()
    week_type_slots = db.session.query(table).filter(table.c.season_id == season_id,
                                                   table.c.day_type == day_type_id,
                                                   table.c.date == total_week_type_slots.date
                                                     ).all()
    result = list()
    for slot in week_type_slots:
        d = dict()
        d['tee_time'] = slot.tee_time.strftime('%H:%M')
        d['hole_9_price'] = str(slot.hole_9_price) if slot.hole_9_price else "",
        d['hole_18_price'] = str(slot.hole_18_price) if slot.hole_18_price else "",
        result.append(d)
    return result


def update_week_type_slots(gc_id, json_data):
    day_type = json_data.get('day_type')
    season_id = json_data.get('season_id')
    days = json_data.get('days')
    days = tuple(days)
    slots = json_data.get('slots')
    table =  get_gc_slot_table_object("gc_{}_slots".format(gc_id))
    for slot in slots:
        tee_time = slot.get('tee_time')
        hole_9_price = slot.get('hole_9_price',None)
        hole_18_price = slot.get('hole_18_price',None)
        hole_9_flag = slot.get('hole_9_flag')
        hole_18_flag = slot.get('hole_18_flag')
        if not hole_9_flag:
            hole_9_price = None
        else:
            hole_9_price = float(hole_9_price)
        if not hole_18_flag:
            hole_18_price = None
        else:
            hole_18_price = float(hole_18_price)
        slot_status = slot.get('slot_status',None)
        if not slot_status:
            slot_status = 'OPEN'
        #tee_slots = db.session.query(table).filter(table.c.tee_time == tee_time,
        #                                           table.c.season_id == season_id,
        #                                           table.c.day_type == day_type).all()
        db.session.execute(
            "update \"gc_{}_slots\" set hole_9_price = {}, hole_18_price = {} , slot_status = '{}' where tee_time = '{}' and season_id = '{}' and day_type = '{}' and day in '{}' ;"
                .format(gc_id, hole_9_price, hole_18_price, slot_status, tee_time, season_id, day_type, days),
            bind=db.get_engine(app, 'base_db'))
        db.session.commit()

def get_date_wise_slot(gc_id, query_data):
    date = query_data.get("date")
    date_obj = datetime.strptime(date,'%Y-%m-%d').date()
    if not date:
        return None
    table = get_gc_slot_table_object("gc_{}_slots".format(gc_id))
    date_slots = db.session.query(table).filter(
        table.c.date == date_obj
    ).all()
    result = list()
    if not date_slots:
        return result
    for slot in date_slots:
        d = dict()
        d['id'] = slot.id
        d['tee_time'] = slot.tee_time.strftime('%H:%M')
        d['hole_9_price'] = slot.hole_9_price
        d['hole_18_price'] = slot.hole_18_price
        d['slot_status'] = slot.slot_status
        result.append(d)
    return result

def update_date_wise_slot(gc_id, json_data):
    table = get_gc_slot_table_object("gc_{}_slots".format(gc_id))
    slots = json_data.get('slots')
    for slot in slots:
        slot_id = slot.get('id')
        hole_9_price = slot.get('hole_9_price',None)
        hole_18_price = slot.get('hole_18_price',None)
        hole_9_flag = slot.get('hole_9_flag',None)
        hole_18_flag = slot.get('hole_18_flag',None)
        if not hole_9_flag:
            hole_9_price = None
        if not hole_18_flag:
            hole_18_price = None
        slot_status = slot.get('slot_status',None)
        if not slot_status:
            slot_status = 'OPEN'
        db.session.execute(
            "update \"gc_{}_slots\" set hole_9_price = {}, hole_18_price = {} , slot_status = '{}' where id = '{}';"
                .format(gc_id, hole_9_price, hole_18_price, slot_status, slot_id),
            bind=db.get_engine(app, 'base_db'))
    if len(slots) > 0:
        db.session.commit()

def apply_holiday(gc_id, dates):
    from odyssey.v1.models.gc_rates_info import GCRatesInfo
    from odyssey.v1.models.days_type_info import DaysTypeInfo
    table = get_gc_slot_table_object("gc_{}_slots".format(gc_id))
    weekend_id = DaysTypeInfo.query.filter(DaysTypeInfo.day_type =="weekend").first().id
    try:
        for date in dates:
            table_data = db.session.query(table.c.season_id,table.c.day_type).filter(table.c.date == date).first()
            if table_data and table_data.day_type == weekend_id:
                continue
            else:
                weekend_rate_info = GCRatesInfo.query.filter(GCRatesInfo.season_id == table_data.season_id,
                                                             GCRatesInfo.gc_id == gc_id,
                                                             GCRatesInfo.day_type == weekend_id).first()
                db.session.execute("update \"gc_{}_slots\" set hole_9_price = {}, hole_18_price = {} where date = '{}' ;".format(
                    gc_id, weekend_rate_info.hole_9_price, weekend_rate_info.hole_18_price, date),bind=db.get_engine(app, 'base_db'))
                db.session.commit()
    except:
        app.logger.info("error in holiday apply")
        import traceback
        db.session.rollback()
        app.logger.error(traceback.print_exc())

def create_holiday_days(gc_id, json_data):
    from odyssey.v1.models.gc_holidays_info import GCHolidaysDaysInfo
    data = json_data.get("data")
    dates = list()
    for info in data:
        date = info.get("date")
        date = datetime.strptime(date,"%Y-%m-%d").date()
        name = info.get("name")
        all_flag = info.get("universal",False)
        obj = GCHolidaysDaysInfo(
            id = generate_id(),
            gc_id=gc_id,
            date=date,
            name=name,
            all=all_flag
        )
        db.session.add(obj)
        dates.append(date)
    db.session.commit()
    apply_holiday(gc_id, dates)

def update_holiday_days(gc_id, json_data):
    from odyssey.v1.models.gc_holidays_info import GCHolidaysDaysInfo
    data = json_data.get("data")
    dates = list()
    for info in data:
        date = info.get("date")
        uid  = info.get("id")
        date = datetime.strptime(date,"%Y-%m-%d").date()
        name = info.get("name")
        all_flag = info.get("universal",False)
        obj = GCHolidaysDaysInfo.query.get(uid)
        if obj:
            obj.date = date
            obj.name = name
            obj.universal = all_flag
            db.session.add(obj)
        dates.append(date)
    db.session.commit()
    apply_holiday(gc_id, dates)

def apply_closed(gc_id, dates):
    try:
        for date in dates:
            d = date[0]
            t = date[1]
            if t:
                db.session.execute("update \"gc_{}_slots\" set slot_status = 'CLOSED' where date = '{}' and tee_time < '{}' ;".format(
                    gc_id,d,t),bind=db.get_engine(app, 'base_db'))
            else:
                db.session.execute(
                    "update \"gc_{}_slots\" set slot_status = 'CLOSED' where date = '{}' ;".format(
                        gc_id, d), bind=db.get_engine(app, 'base_db'))
            db.session.commit()
    except:
        app.logger.info("error in closed apply")
        import traceback
        db.session.rollback()
        app.logger.error(traceback.print_exc())

def create_closed_days(gc_id, json_data):
    from odyssey.v1.models.gc_closed_days_info import GCClosedDaysInfo
    data = json_data.get("data")
    dates = list()
    for info in data:
        date = info.get("date")
        full_day = info.get("full_day",False)
        start_time = None
        if full_day:
            obj = GCClosedDaysInfo(
                id=generate_id(),
                date= datetime.strptime(date,'%Y-%m-%d'),
                gc_id=gc_id,
                full_day=full_day,
                start_time=None
            )
        else:
            start_time = info.get('start_time')
            start_time = datetime.strptime(start_time, '%H:%M').time()
            obj = GCClosedDaysInfo(
                id=generate_id(),
                date=date,
                gc_id=gc_id,
                full_day=full_day,
                start_time=start_time
            )
        db.session.add(obj)
        dates.append([date,start_time])
    db.session.commit()
    apply_closed(gc_id, dates)

def update_closed_days(gc_id, json_data):
    from odyssey.v1.models.gc_closed_days_info import GCClosedDaysInfo
    data = json_data.get("data")
    dates = list()
    for info in data:
        date = info.get("date")
        uid  = info.get("id")
        full_day = info.get("full_day",None)
        start_time = None
        obj = GCClosedDaysInfo.query.get(uid)
        if obj:
            if full_day and full_day == True:
                obj.full_day = full_day
                obj.start_time = None
                obj.date = datetime.strptime(date,'%Y-%m-%d')
            else:
                start_time = info.get('start_time')
                start_time = datetime.strptime(start_time, '%H:%M').time()
                obj.full_day = False
                obj.start_time = start_time
                obj.date = datetime.strptime(date, '%Y-%m-%d')
            db.session.add(obj)
            dates.append([date,start_time])
    db.session.commit()
    apply_closed(gc_id, dates)

def update_day_types(gc_id, weekdays, weekends):
    try:
        weekdays = weekdays.split(',')
        weekends = weekends.split(',')
        weekdays = tuple(weekdays)
        weekends = tuple(weekends)
        days_type = DaysTypeInfo.query.filter(DaysTypeInfo.day_type.in_(['weekday', 'weekend'])).order_by(
            DaysTypeInfo.day_type).all()
        weekday_id = days_type[0].id
        weekend_id = days_type[0].id
        db.session.execute("update \"gc_{}_slots\" set day_type = '{}' where day in '{}' ;".format(
                        gc_id, weekday_id,weekdays), bind=db.get_engine(app, 'base_db'))
        db.session.execute("update \"gc_{}_slots\" set day_type = '{}' where day in '{}' ;".format(
            gc_id, weekend_id, weekends), bind=db.get_engine(app, 'base_db'))
        db.session.commit()
    except:
        import traceback
        app.logger.info("error in updating weekday weekends")
        app.logger.error(traceback.print_exc())

def update_weekly_off_day(gc_id, day):
    try:
        if not gc_id or not day:
            return
        db.session.execute("update \"gc_{}_slots\" set slot_status = '{}' where slot_status = '{}' ;".format(
            gc_id,'OPEN','WEEKLY_OFF'), bind=db.get_engine(app, 'base_db'))
        db.session.execute("update \"gc_{}_slots\" set slot_status = '{}' where day = '{}' ;".format(
            gc_id, 'WEEKLY_OFF', day), bind=db.get_engine(app, 'base_db'))
        db.session.commit()
    except:
        import traceback
        app.logger.info("error in updating maintenance day")
        app.logger.error(traceback.print_exc())

def update_season_dates_slot(gc_id):
    return