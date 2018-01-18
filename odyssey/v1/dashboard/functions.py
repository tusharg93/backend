def load_home_page_data(gc_id):
    from odyssey.v1.models.golf_course_master import GolfCourseMaster
    from odyssey.v1.models.gc_seasons_info import GCSeasonsInfo
    from odyssey.v1.models.gc_special_days_info import GCSpecialDaysInfo
    from odyssey.v1.models.gc_rates_info import GCRatesInfo

    gc_base_obj = GolfCourseMaster.query.filter(GolfCourseMaster.id == gc_id).first()
    if not gc_base_obj:
        return
    result = dict()
    result['basic_info'] = gc_base_obj.dashboard_serialize
    gc_special_days_obj = GCSpecialDaysInfo.query.filter(GCSpecialDaysInfo.gc_id == gc_id).all()
    if gc_special_days_obj:
        result['maintenance_info'] = [x.serialize for x in gc_special_days_obj]
    gc_seasons_obj = GCSeasonsInfo.query.filter(GCSeasonsInfo.gc_id == gc_id).first()
    
