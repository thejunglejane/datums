# -*- coding: utf-8 -*-

from functools import wraps
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


def database_setup(engine):
    '''Set up the database.
    '''
    metadata.create_all(engine)


def database_teardown(engine):
    '''BURN IT ALL DOWN (╯°□°）╯︵ ┻━┻
    '''
    metadata.drop_all(engine)


def _action_and_commit(obj, action):
    '''Adds/deletes the instance obj to/from the session based on the action.
    '''
    action(obj)
    session.commit()


class GhostBase(Base):

    '''The GhostBase class extends the declarative Base class.'''

    __abstract__ = True

    def __str__(self, attrs):
        return '''<{0}({1})>'''.format(self.__class__.__name__, ', '.join([
            '='.join([attr, str(getattr(self, attr, ''))]) for attr in attrs]))

    @classmethod
    def _get_instance(cls, **kwargs):
        '''Returns the first instance of cls with attributes matching **kwargs.
        '''
        return session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def get_or_create(cls, **kwargs):
        '''
        If a record matching the instance already exists in the database, then
        return it, otherwise create a new record.
        '''
        q = cls._get_instance(**kwargs)
        if q:
            return q
        q = cls(**kwargs)
        _action_and_commit(q, session.add)
        return q

    @classmethod
    def update(cls, snapshot, **kwargs):
        '''
        If a record matching the instance id already exists in the database, 
        update it. If a record matching the instance id does not already exist,
        create a new record.
        '''
        q = cls._get_instance(**kwargs)
        if q:
            for k in snapshot:
                setattr(q, k, snapshot[k])
            _action_and_commit(q, session.add)
        else:
            cls.get_or_create(**kwargs)

    @classmethod
    def delete(cls, **kwargs):
        '''
        If a record matching the instance id exists in the database, delete it.
        '''
        q = cls._get_instance(**kwargs)
        if q:
            _action_and_commit(q, session.delete)


class ResponseClassLegacyAccessor(object):

    def __init__(self, response_class, column, accessor):
        self.response_class = response_class
        self.column = column
        self.accessor = accessor

    def _get_instance(self, **kwargs):
        '''Return the first existing instance of the response record.
        '''
        return session.query(self.response_class).filter_by(**kwargs).first()

    def get_or_create_from_legacy_response(self, response, **kwargs):
        '''
        If a record matching the instance already does not already exist in the
        database, then create a new record.
        '''
        response_cls = self.response_class(**kwargs).get_or_create(**kwargs)
        if not getattr(response_cls, self.column):
            setattr(response_cls, self.column, self.accessor(response))
            _action_and_commit(response_cls, session.add)

    def update(self, response, **kwargs):
        '''
        If a record matching the instance already exists in the database, update
        it, else create a new record.
        '''
        response_cls = self._get_instance(**kwargs)
        if response_cls:
            setattr(response_cls, self.column, self.accessor(response))
            _action_and_commit(response_cls, session.add)
        else:
            self.get_or_create_from_legacy_response(response, **kwargs)

    def delete(self, response, **kwargs):
        '''
        If a record matching the instance id exists in the database, delete it.
        '''
        response_cls = self._get_instance(**kwargs)
        if response_cls:
            _action_and_commit(response_cls, session.delete)


class LocationResponseClassLegacyAccessor(ResponseClassLegacyAccessor):

    def __init__(
            self, response_class, column,
            accessor, venue_column, venue_accessor):
        super(LocationResponseClassLegacyAccessor, self).__init__(
            response_class, column, accessor)
        self.venue_column = venue_column
        self.venue_accessor = venue_accessor

    def get_or_create_from_legacy_response(self, response, **kwargs):
        '''
        If a record matching the instance already does not already exist in the
        database, then create a new record.
        '''
        response_cls = self.response_class(**kwargs).get_or_create(**kwargs)
        if not getattr(response_cls, self.column):
            setattr(response_cls, self.column, self.accessor(response))
            _action_and_commit(response_cls, session.add)
        if not getattr(response_cls, self.venue_column):
            setattr(
                response_cls, self.venue_column, self.venue_accessor(response))
            _action_and_commit(response_cls, session.add)

    def update(self, response, **kwargs):
        '''
        If a record matching the instance already exists in the database, update
        both the column and venue column attributes, else create a new record.
        '''
        response_cls = super(
            LocationResponseClassLegacyAccessor, self)._get_instance(**kwargs)
        if response_cls:
            setattr(response_cls, self.column, self.accessor(response))
            setattr(
                response_cls, self.venue_column, self.venue_accessor(response))
            _action_and_commit(response_class, session.add)
