from sqlalchemy import (Column, Date, Integer, String)

from common.db.helpers import JsonField, Tables, TimestampField
from layer.common.db.models.base import BaseModel


class UserBase(object):
    email = Column('email', String(256))
    # Even uuid is deleted from Base model it will still remain in userBase
    # uuid = Column('uuid', String(128), info='Cognito user pool id')


class UserModel(UserBase, BaseModel):
    __tablename__ = Tables.USERS.value

    # user_id will saved in uuid column of parent
    first_name = Column('first_name', String(256))
    last_name = Column('last_name', String(256))
    identityId = Column('identityId', String(256), info='Cognito identification id')
    username = Column('username', String(20), info='User mobile number')

    city_id = Column('city_id', Integer())
    dob = Column('dob', Date())
    payment = Column('payment', JsonField())
    platform = Column('platform', String(50))
    tos_acceptance_ip = Column('tos_acceptance_ip', String(50))
    tos_acceptance_time = Column('tos_acceptance_time', TimestampField())

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
