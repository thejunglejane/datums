from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import os

# Initialize Base class
Base = declarative_base()
metadata = Base.metadata

session_maker = sessionmaker()
session = scoped_session(session_maker)

engine = create_engine(os.environ['DATABASE_URI'])
session.configure(bind=engine)


class GhostBase(Base):

    '''The GhostBase class extends the declarative Base class.'''

    __abstract__ = True

    @classmethod
    def get_or_create(cls, **kwargs):
        '''
        If a record matching the instance already exists in the database, then
        return it, otherwise create a new record.
        '''
        q = session.query(cls).filter_by(**kwargs).first()
        if q:
            return q
        q = cls(**kwargs)
        session.add(q)
        session.commit()
        return q


class ResponseClassLegacyAccessor(object):

    def __init__(self, response_class, column, accessor):
        self.response_class = response_class
        self.column = column
        self.accessor = accessor

    def get_or_create_from_legacy_response(self, response, **kwargs):
        response_cls = self.response_class(**kwargs)
        # Return the existing or newly created response record for the unique
        # question_id, snapshot_id pair
        response_cls = response_cls.get_or_create(**kwargs)
        # If the record does not have a response, add it
        if not getattr(response_cls, self.column):
            setattr(response_cls, self.column, self.accessor(response))
            session.add(response_cls)
            session.commit()


def database_setup(engine):
    # Set up the database
    metadata.create_all(engine)


def database_teardown(engine):
    # BURN IT TO THE GROUND
    metadata.drop_all(engine)
