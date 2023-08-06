import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.aws import get_secret_value

DB_SECRET_KEY = os.environ.get('db_secret')


def create_session():
    engine = create_engine(
        get_secret_value(DB_SECRET_KEY),
        echo=True, echo_pool=True,
        pool_size=1,
        pool_timeout=60,
        encoding='UTF-8',
        convert_unicode=True,
    )
    return sessionmaker(bind=engine, autocommit=True, )()
