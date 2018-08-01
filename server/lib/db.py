from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, Float, String, Text, Boolean, text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()
metadata = Base.metadata


def dbconnect(options):

    engine = create_engine('sqlite:///%s' % options['db_file'])
    Session = sessionmaker(bind=engine)
    return Session, engine


def db_create(options):
    sess, engine = dbconnect(options)
    print 'HI'
    metadata.create_all(engine)


class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    address = Column(String(500), nullable=False)
    created_on = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class User(Base):
    #TODO uniqueness
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    school_id = Column(Integer, ForeignKey('school.id'))
    email = Column(String(250), nullable=False)
    created_on = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    school = relationship(School)


class Club(Base):
    __tablename__ = 'club'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    school_id = Column(Integer, ForeignKey('school.id'))
    description = Column(String(1024), nullable=False)
    created_on = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    school = relationship(School)


class UserToClubMapping(Base):
    __tablename__ = 'user_to_club_mapping'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    club_id = Column(Integer, ForeignKey('club.id'))
    is_admin = Column(Boolean, server_default=text("FALSE"))
    created_on = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship(User)
    club = relationship(Club)
