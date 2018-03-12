from odyssey import db, app
from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import TIME

def create_gc_slot_table(gc_id):
    query = 'CREATE TABLE IF NOT EXISTS "gc_{}_slots" AS SELECT * FROM slots_master'.format(gc_id)
    db.session.execute(query, bind=db.get_engine(app, 'base_db'))
    db.session.commit()
    db.get_binds()


def get_gc_slot_table_object(table_name):
    db.session.bind = db.get_engine(app, 'base_db')
    return db.Table(
        table_name,
        MetaData(),
        db.Column('id', db.String, primary_key=True),
        db.Column('day',db.String),
        db.Column('date', db.Date),
        db.Column('tee_time', TIME()),
        db.Column('day_type',db.String),
        db.Column('hole_9_price', db.Float),
        db.Column('hole_18_price', db.Float),
        db.Column('season_id',db.String),
        db.Column('status',db.String),
        db.Column('min_golfers',db.Integer)
    )

def get_gc_table_class_object(table_name):
    return type(table_name, (db.Model,),
    {
        '__tablename__': table_name,
        '__table_args__': {'extend_existing': True},
        'id':  db.Column('id', db.String, primary_key=True),
        'day':db.Column('day',db.String),
        'date':db.Column('date', db.Date),
        'tee_time':db.Column('tee_time', TIME()),
        'day_type':db.Column('day_type',db.String),
        'hole_9_price':db.Column('hole_9_price', db.Float),
        'hole_18_price':db.Column('hole_18_price', db.Float),
        'season_id':db.Column('season_id',db.String),
        'status':db.Column('status', db.String),
        'min_golfers':db.Column('min_golfers',db.Integer)

    }
     )