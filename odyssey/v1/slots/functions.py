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
    gc_info =  db.session.query(GolfCourseMaster.id,GolfCourseMaster.duration_live_slots,GolfCourseMaster.weekends,GolfCourseMaster.weekdays, GolfCourseMaster.time_zone, GolfCourseMaster.min_weekdays, GolfCourseMaster.min_weekends, GolfCourseMaster.maintenance_day, GolfCourseMaster.maintenance_type, GolfCourseMaster.hole_18_flag, GolfCourseMaster.hole_9_flag).filter(GolfCourseMaster.id == gc_id).first()
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
    weekend_id = days_type[1].id
    current_year = today_year
    maintenance_day = gc_object.maintenance_day
    maintenance_type = gc_object.maintenance_type
    for gc_season_details in gc_seasons_obj:
        start_date = gc_season_details.start_date
        end_date = gc_season_details.end_date
        season_id = gc_season_details.season_id
        maintenance_stime = None
        maintenance_etime = None
        if maintenance_type == True:
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
                    status = 'CLOSED'
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
                        if status == 'CLOSED':
                            if not maintenance_stime:
                                d['status'] = status
                            else:
                                if current_start >= special_stime and current_start <= special_etime:
                                    d['status'] = status
                                else:
                                    d['status'] = 'OPEN'
                        else:
                            d['status'] = 'OPEN'
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
    table = get_gc_table_class_object("gc_{}_slots".format(gc_id))
    season_id = query_params.get("season_id")
    day_type_id = query_params.get("day_type")
    m_day = GolfCourseMaster.query.filter(GolfCourseMaster.id == gc_id).first().maintenance_day
    days = query_params.get("days")
    if days:
        if m_day and m_day in days:
            days.remove(m_day)
        days = tuple(days)
    # gc_season_info = db.session.query(GCSeasonsInfo.start_time,GCSeasonsInfo.end_time, GCSeasonsInfo.tee_interval).filter(
    #     GCSeasonsInfo.gc_id == gc_id,
    #     GCSeasonsInfo.season_id == season_id
    # ).first()
    # gc_rates_info = GCRatesInfo.query.filter(GCRatesInfo.season_id == season_id,
    #                                          GCRatesInfo.gc_id == gc_id,
    #                                          GCRatesInfo.day_type == day_type_id).first()
    # date = datetime.today().date()
    # start_time = datetime.combine(date,gc_season_info.start_time)
    # end_time = datetime.combine(date,gc_season_info.end_time)
    if days:
        slot_data = table.query.filter(table.season_id == season_id,table.day.in_(days)).distinct(table.tee_time).all()
    else:
        slot_data = table.query.filter(table.season_id == season_id).distinct(
            table.tee_time).all()

    #interval = gc_season_info.tee_interval
    result = list()
    for slot in slot_data:
        d = dict()
        d['tee_time'] = slot.tee_time.strftime('%H:%M')
        d['hole_9_price'] = slot.hole_9_price
        d['hole_18_price'] = slot.hole_18_price
        d['slot_status'] = slot.status
        result.append(d)
    return result


def update_week_type_slots(gc_id, json_data):
    day_type = json_data.get('day_type')
    season_id = json_data.get('season_id')
    days = json_data.get('days')
    m_day = GolfCourseMaster.query.filter(GolfCourseMaster.id == gc_id).first().maintenance_day
    if m_day and m_day in days:
        days.remove(m_day)
    days = tuple(days)
    slots = json_data.get('slots')
    table =  get_gc_table_class_object("gc_{}_slots".format(gc_id))
    for slot in slots:
        tee_time = datetime.strptime(slot.get('tee_time'),"%H:%M").time()
        hole_9_price = slot.get('hole_9_price',None)
        hole_18_price = slot.get('hole_18_price',None)
        status = slot.get('slot_status')


        tee_slots = db.session.query(table).filter(table.tee_time == tee_time,
                                                  table.season_id == season_id,
                                                  table.day_type == day_type,
                                                  table.day.in_(days)).all()
        if tee_slots:
            for slot_data in tee_slots:
                slot_data.hole_9_price = hole_9_price
                slot_data.hole_18_price = hole_18_price
                slot_data.status = status
                db.session.add(slot_data)
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
        d['slot_status'] = slot.status
        result.append(d)
    return result

def update_date_wise_slot(gc_id, json_data):
    table = get_gc_table_class_object("gc_{}_slots".format(gc_id))
    slots = json_data.get('slots')
    update_dict = dict()
    for slot in slots:
        slot_id = slot.get('id')
        hole_9_price = slot.get('hole_9_price',None)
        hole_18_price = slot.get('hole_18_price',None)
        status = slot.get('slot_status',None)

        update_dict[slot_id] = dict()
        update_dict[slot_id]['hole_9_price'] = hole_9_price
        update_dict[slot_id]['hole_18_price'] = hole_18_price
        update_dict[slot_id]['slot_status'] = status
    slot_ids = update_dict.keys()
    tee_slots = db.session.query(table).filter(table.id.in_(slot_ids)).all()
    for slot in tee_slots:
        data = update_dict[slot.id]
        slot.hole_9_price = data['hole_9_price']
        slot.hole_18_price = data['hole_18_price']
        slot.status = data['slot_status']
        db.session.add(slot)
    if tee_slots:
        db.session.commit()

def apply_holiday(gc_id, dates):
    from odyssey.v1.models.gc_rates_info import GCRatesInfo
    from odyssey.v1.models.days_type_info import DaysTypeInfo
    table = get_gc_table_class_object("gc_{}_slots".format(gc_id))
    weekend_id = DaysTypeInfo.query.filter(DaysTypeInfo.day_type =="weekend").first().id
    try:
        for date in dates:
            table_data = table.query.filter(table.date == date).first()
            if table_data:
                if table_data.day_type == weekend_id:
                    continue
                else:
                    weekend_rate_info = GCRatesInfo.query.filter(GCRatesInfo.season_id == table_data.season_id,
                                                             GCRatesInfo.gc_id == gc_id,
                                                             GCRatesInfo.day_type == weekend_id).first()
                    table_data = table.query.filter(table.date == date).all()
                    for slot in table_data:
                        if slot.hole_9_price is not None:
                            slot.hole_9_price = weekend_rate_info.hole_9_price
                        if slot.hole_18_price is not None:
                            slot.hole_18_price = weekend_rate_info.hole_18_price
                        db.session.add(slot)
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
        if uid:
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
    table = get_gc_table_class_object("gc_{}_slots".format(gc_id))
    try:
        for date_obj in dates:
            date = date_obj[0]
            start_tee = date_obj[1]
            end_tee = date_obj[2]
            if start_tee:
                slot_data = table.query.filter(table.date == date, table.tee_time >= start_tee, table.tee_time <= end_tee).all()
                if slot_data:
                    for slot in slot_data:
                        slot.status = 'CLOSED'
                        db.session.add(slot)
            else:
                slot_data = table.query.filter(table.date == date).all()
                if slot_data:
                    for slot in slot_data:
                        slot.status = 'CLOSED'
                        db.session.add(slot)
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
        date = datetime.strptime(date,'%Y-%m-%d')
        full_day = info.get("full_day",False)
        start_time = None
        end_time = None
        if full_day:
            obj = GCClosedDaysInfo(
                id=generate_id(),
                date=date ,
                gc_id=gc_id,
                full_day=full_day,
                start_time=None
            )
            obj.end_time = None
        else:
            start_time = info.get('start_time')
            end_time = info.get('end_time',None)
            start_time = datetime.strptime(start_time, '%H:%M').time()
            if end_time:
                end_time = datetime.strptime(end_time, '%H:%M').time()
            obj = GCClosedDaysInfo(
                id=generate_id(),
                date=date,
                gc_id=gc_id,
                full_day=full_day,
                start_time=start_time
            )
            obj.end_time = end_time
        db.session.add(obj)
        dates.append([date,start_time, end_time])
    db.session.commit()
    apply_closed(gc_id, dates)

def update_closed_days(gc_id, json_data):
    from odyssey.v1.models.gc_closed_days_info import GCClosedDaysInfo
    data = json_data.get("data")
    dates = list()
    for info in data:
        date = info.get("date")
        date = datetime.strptime(date,'%Y-%m-%d')
        uid  = info.get("id")
        full_day = info.get("full_day",None)
        start_time = None
        end_time = None
        obj = GCClosedDaysInfo.query.get(uid)
        if obj:
            if full_day and full_day == True:
                obj.full_day = full_day
                obj.start_time = None
                obj.end_time = None
                obj.date = date
            else:
                start_time = info.get('start_time')
                start_time = datetime.strptime(start_time, '%H:%M').time()
                end_time = info.get('end_time', None)
                if end_time:
                    end_time = datetime.strptime(end_time, '%H:%M').time()
                obj.full_day = False
                obj.start_time = start_time
                obj.end_time = end_time
                obj.date = date
            db.session.add(obj)
            dates.append([date,start_time,end_time])
    db.session.commit()
    apply_closed(gc_id, dates)

def update_day_types(gc_id, weekdays, weekends):
    table = get_gc_table_class_object("gc_{}_slots".format(gc_id))
    try:
        weekdays = weekdays.split(',')
        weekends = weekends.split(',')
        weekdays = tuple(weekdays)
        weekends = tuple(weekends)
        days_type = DaysTypeInfo.query.filter(DaysTypeInfo.day_type.in_(['weekday', 'weekend'])).order_by(
            DaysTypeInfo.day_type).all()
        weekday_id = days_type[0].id
        weekend_id = days_type[1].id
        weekday_slot_data = table.query.filter(table.day.in_(weekdays)).all()
        if weekday_slot_data:
            for slot in weekday_slot_data:
                slot.day_type = weekday_id
                db.session.add(slot)
        weekend_slot_data = table.query.filter(table.day.in_(weekends)).all()
        if weekend_slot_data:
            for slot in weekend_slot_data:
                slot.day_type = weekend_id
                db.session.add(slot)
            db.session.commit()
    except:
        import traceback
        app.logger.info("error in updating weekday weekends")
        app.logger.error(traceback.print_exc())

def update_weekly_off_day(gc_id, old_mday, current_mday, full_day):
    table = get_gc_table_class_object("gc_{}_slots".format(gc_id))
    try:
        if not gc_id or table.query.count() == 0:
            return
        if old_mday is not None:
            slots_data = table.query.filter(table.day == old_mday,table.status == 'CLOSED').all()
            for slot in slots_data:
                slot.status = 'OPEN'
                db.session.add(slot)
            db.session.commit()
        if current_mday is not None:
            if full_day == True:
                slots_day_data = table.query.filter(table.day == current_mday).all()
                for slot in slots_day_data:
                    slot.status = 'CLOSED'
                    db.session.add(slot)
            else:
                gc_mtimes = GCSeasonsInfo.query.filter(GCSeasonsInfo.gc_id == gc_id).all()
                for season_data in gc_mtimes:
                    s_time = season_data.maintenance_stime
                    e_time = season_data.maintenance_etime
                    slots_day_data = table.query.filter(table.day == current_mday, table.tee_time >= s_time, table.tee_time <= e_time).all()
                    for slot in slots_day_data:
                        slot.status = 'CLOSED'
                        db.session.add(slot)
            db.session.commit()
    except:
        import traceback
        app.logger.info("error in updating maintenance day")
        app.logger.error(traceback.print_exc())

