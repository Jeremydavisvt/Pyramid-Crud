from sqlalchemy import (
    Column,
    Integer,
    VARCHAR, DATETIME, BOOLEAN, DATE)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'
    uid = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR)
    last_name = Column(VARCHAR)
    dob = Column(DATE)
    zip_code = Column(Integer)
    is_admin = Column(BOOLEAN)
    email = Column(VARCHAR)
    password = Column(VARCHAR)
    created_ts = Column(DATETIME)


