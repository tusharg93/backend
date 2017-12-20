from odyssey import db, app
from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import TIME

def create_gc_slot_table(gc_id):
    query = 'CREATE TABLE IF NOT EXISTS "gc_{}_slots" AS SELECT * FROM slots_mater'.format(gc_id)
    db.session.execute(query, bind=db.get_engine(app, 'base_db'))
    db.session.commit()


def get_gc_slot_table_object(table_name):
    db.session.bind = db.get_engine(app, 'base_db')
    return db.Table(
        table_name,
        MetaData(),
        db.Column('id', db.String, primary_key=True),
        db.Column('date', db.Date),
        db.Column('tee_time', TIME()),
        db.Column('day_type',db.String),
        db.Column('hole_9_price', db.Float),
        db.Column('hole_18_price', db.Float),
        db.Column('season_id',db.String),
        db.Column('slot_status', db.String),
        db.Column('min_golfers',db.Integer)
    )