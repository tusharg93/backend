def load_home_page_data(gc_id):
    from odyssey.v1.models.golf_course_master import GolfCourseMaster
    from odyssey.v1.models.gc_seasons_info import GCSeasonsInfo
    from odyssey.v1.models.gc_special_days_info import GCSpecialDaysInfo
    from odyssey.v1.models.gc_rates_info import GCRatesInfo
    from odyssey.v1.models.season_master import SeasonsMaster
    from odyssey import db
    from odyssey.v1.common.functions import get_default_values
    import datetime

    gc_base_obj = GolfCourseMaster.query.filter(GolfCourseMaster.id == gc_id).first()
    if not gc_base_obj:
        return
    result = dict()
    result['gc_basic_info'] = gc_base_obj.dashboard_serialize
    gc_special_days_obj = GCSpecialDaysInfo.query.filter(GCSpecialDaysInfo.gc_id == gc_id).all()
    if gc_special_days_obj:
        result['maintenance_info'] = [x.serialize for x in gc_special_days_obj]
    gc_seasons_obj = db.session.query(GCSeasonsInfo,SeasonsMaster).filter(GCSeasonsInfo.gc_id == gc_id,
                                                                          GCSeasonsInfo.season_id == SeasonsMaster.id).all()
    result['seasons_info'] = list()
    for season in gc_seasons_obj:
        d = dict()
        d['id'] = season.SeasonsMaster.id
        d['name'] = season.SeasonsMaster.name
        d['start_date'] = season.GCSeasonsInfo.start_date.strftime('%m-%d')
        d['end_date'] = season.GCSeasonsInfo.end_date.strftime('%m-%d')
        d['start_time'] = season.GCSeasonsInfo.start_time.strftime('%H:%M')
        d['end_time'] = season.GCSeasonsInfo.end_time.strftime('%H:%M')
        d['tee_interval'] = season.GCSeasonsInfo.tee_interval
        result['seasons_info'].append(d)

    result['rates_info'] = list()
    gc_rates_info = GCRatesInfo.query.filter(GCRatesInfo.gc_id == gc_id).all()
    for rate in gc_rates_info:
        d = dict()
        d['season_id'] = rate.season_id
        d['day_type'] = rate.day_type
        d['hole_9_price'] = rate.hole_9_price
        d['hole_18_price'] = rate.hole_18_price
        result['rates_info'].append(d)
    result['defaults'] = dict()
    default_data = get_default_values()
    if default_data:
        result['defaults'] = default_data
    return result