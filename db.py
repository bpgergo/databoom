from db_params import db_dbname, db_host, db_password, db_user, db_driver_name
#sqlalchemy engine setup with mysql
connect_string = '%s://%s:%s@%s/%s' \
    % (db_driver_name, db_user, db_password, db_host, db_dbname)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
from models import *
import logging
from datetime import datetime
import uuid
from load_metadata import load_func, load_econ
from psycopg2 import IntegrityError
import json
from bson import json_util
import decimal
import json
from parse_budget import generate_rows


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def get_in_json(what):
    return [dict(f) for f in what]


engine = create_engine(connect_string) #, pool_recycle=60)
# create.sql a configured "Session" class
Session = sessionmaker(bind=engine)


def save_item(session, item):
    if item.id is None:
        item.id = str(uuid.uuid1())
    session.add(item)
    return item


def get_func(session, value):
    return session.query(Func).filter(Func.value == value).first()


def save_func(session, name, parent=None):
    item = Func(value=name)
    saved = get_func(session, name)
    if saved is None:
        if parent and parent.id:
            item.parent_id = parent.id
        saved = save_item(session, item)
    return saved


def get_econ(session, value):
    return session.query(Econ).filter(Econ.value == value).first()



def get_econ_ids():
    result = set()
    for econ in get_all_econ():
        result.add(econ.id)
    return result


def get_parent_econ_ids():
    result = set()
    for econ in get_all_econ():
        result.add(econ.parent_id)
    return result


def save_econ(session, name, parent=None):
    item = Econ(value=name)
    saved = get_econ(session, name)
    if saved is None:
        if parent and parent.id:
            item.parent_id = parent.id
        saved = save_item(session, item)
    return saved


def get_econ_by_id(session, id):
    return session.query(Econ).filter(Econ.id == id).first()


def get_org(session, value):
    return session.query(Org).filter(Org.value == value).first()


def save_org(session, name, parent=None):
    item = Org(value=name)
    saved = get_org(session, name)
    if saved is None:
        if parent and parent.id:
            item.parent_id = parent.id
        saved = save_item(session, item)
    return saved


def save_budget(session, amount, func, econ, org, date_start, date_end, comments, tags):
    budget = Budget(func_id=func.id, econ_id=econ.id, amount=amount, org_id=org.id, date_start=date_start, date_end=date_end, comm=comments, tags=tags)
    return save_item(session, budget)


def get_all_funcs():
    result = engine.execute(Func.__table__.select().order_by(Func.value))
    return result


def get_all_org():
    result = engine.execute(Org.__table__.select().order_by(Org.value))
    return result


def get_all_budget():
    result = engine.execute(Budget.__table__.select().order_by(Budget.id))
    return result


def get_all_econ():
    result = engine.execute(Econ.__table__.select().order_by(Econ.value))
    return result


def load_funcs(session, fname):
    for func in load_func("func_ids.txt"):
        try:
            session.add(func)
            session.commit()
            logging.info("imported func:%s" % func)
        except:
            session.rollback()


def load_econs(session):
    #for econ in reversed(list(load_econ())):
    #    print(econ)

    for econ in list(load_econ()):
        try:
            from_db = get_econ_by_id(session, econ.id)
            if from_db is None:
                session.add(econ)
                session.commit()
                logging.info("imported econ:%s" % econ)
            else:
                logging.info(" ALREADY IN DB econ:%s" % econ)

        except IntegrityError as ie:
            logging.error("Will try again :%s  Exception:%s" % (econ, str(ie)))
            session.rollback()
        except Exception as e:
            logging.error("      ????:%s  Exception:%s" % (econ, str(e)))
            session.rollback()


def load_metadata():
    sess = Session()
    load_funcs(sess, "func_ids.txt")
    load_econs(sess)
    sess.close()


def test_create_budget():
    sess = Session()
    org = save_org(sess, "Zugló")
    sess.commit()
    logging.info("saved Org id:%s" % (org))
    budget = Budget(func_id="011120", econ_id="245", amount=1122.3344, org_id=org.id,
                    date_start=datetime.now(), comm="comments comments comments comments in new line", tags="tag1, tag, tag3")

    save_item(session=sess, item=budget)
    budget = Budget(func_id="011320", econ_id="270", amount=444444.44, org_id=org.id,
                    date_start=datetime.now(), comm="comments comments comments comments in new line", tags="tag1, tag, tag3")
    save_item(session=sess, item=budget)

    sess.commit()
    sess.close()


def load_budget(org_id, dt):
    sess = Session()
    sess.query(Budget).filter(Budget.org_id == org_id).delete()
    sess.flush()
    sess.commit()
    parent_ids = get_parent_econ_ids()
    econ_ids = get_econ_ids()

    #print(parent_ids)
    for budget in generate_rows(org_id, dt, "databoom-budget.csv", econ_ids - parent_ids):
        logging.info("    new budget:%s" % budget)
        save_item(session=sess, item=budget)
        sess.commit()
    sess.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    load_metadata()
    sess = Session()
    org = save_org(sess, "Zugló")
    sess.flush()
    sess.commit()

    dt = datetime.now()
    load_budget(org.id, dt)

