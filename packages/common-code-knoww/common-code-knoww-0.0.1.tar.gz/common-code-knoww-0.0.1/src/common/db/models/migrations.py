from sqlalchemy import (Column, Integer, String)

from common.db.helpers import Tables
from common.db.models import BaseModel


class Migrations(BaseModel):
    __tablename__ = Tables.MIGRATIONS.value
    # Brand details
    m_index = Column('m_index', Integer(), unique=True)
    m_name = Column('m_name', String(256))
