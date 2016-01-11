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


def _validate_and_commit(obj, action, **kwargs):
    '''Adds/deletes the instance obj to/from the session based on the action.
    Validates the values of the attributes in **kwargs against the attributes
    of the instance. If all values are validated, the session will commit,
    otherwise it will rollback.
    '''
    action(obj)
    try:
        for key, value in kwargs.iteritems():
            assert getattr(obj, key) == value
    except (AttributeError, AssertionError), e:
        session.rollback()
        raise e
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
        _validate_and_commit(q, session.add, **kwargs)
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
            _validate_and_commit(q, session.add, **snapshot)
        else:
            cls.get_or_create(**kwargs)

    @classmethod
    def delete(cls, **kwargs):
        '''
        If a record matching the instance id exists in the database, delete it.
        '''
        q = cls._get_instance(**kwargs)
        if q:
            _validate_and_commit(q, session.delete, **kwargs)


class ResponseClassLegacyAccessor(object):

    def __init__(self, response_class, column, accessor):
        self.response_class = response_class
        self.column = column
        self.accessor = accessor

    @staticmethod
    def _confirm_or_add_response(self, obj, attr, response, action, **kwargs):
        try:
            getattr(obj, attr)
        except AttributeError:
            setattr(obj, attr, self.accessor(response))
            self._update_validate_and_commit(
                obj, attr, response, action, **kwargs)

    def _update_validate_and_commit(
            self, obj, attr, response, action, **kwargs):
        '''Update the **kwargs argument before validating and committing/rolling
        back the result.
        '''
        kwargs.update({attr: self.accessor(response)})
        _validate_and_commit(obj, action, **kwargs)

    def get_or_create_from_legacy_response(self, response, **kwargs):
        response_cls = self.response_class(**kwargs).get_or_create(**kwargs)
        self._confirm_or_add_response(
            response_cls, self.column, response, session.add, **kwargs)

    def update(self, response, **kwargs):
        response_cls = self.response_class(**kwargs)
        # Return the existing response record
        response_cls = session.query(
            response_cls.__class__).filter_by(**kwargs).first()
        if response_cls:
            self._confirm_or_add_response(
                response_cls, self.column, response, session.add, **kwargs)
        else:
            response_cls.get_or_create_from_legacy_response(response, **kwargs)

    def delete(self, response, **kwargs):
        response_cls = self.response_class(**kwargs)
        # Return the existing response record
        response_cls = session.query(
            response_cls.__class__).filter_by(**kwargs).first()
        if response_cls:
            _validate_and_commit(response_cls, session.delete, **kwargs)


class LocationResponseClassLegacyAccessor(ResponseClassLegacyAccessor):

    def __init__(
            self, response_class, column,
            accessor, venue_column, venue_accessor):
        super(LocationResponseClassLegacyAccessor, self).__init__(
            response_class, column, accessor)
        self.venue_column = venue_column
        self.venue_accessor = venue_accessor

    def get_or_create_from_legacy_response(self, response, **kwargs):
        response_cls = self.response_class(**kwargs).get_or_create(**kwargs)
        # If the record does not have responses, add them
        try:
            getattr(response_cls, self.column)
        except AttributeError:
            setattr(response_cls, self.column, self.accessor(response))
            kwargs.update({self.column: self.accessor(response)})
            self._validate_and_commit(response_cls, session.add, **kwargs)
        try:
            getattr(response_cls, self.venue_column)
        except AttributeError:
            setattr(
                response_cls, self.venue_column, self.venue_accessor(response))
            kwargs.update({self.venue_column: self.venue_accessor(response)})
            self._validate_and_commit(response_cls, session.add, **kwargs)

    def update(self, response, **kwargs):
        response_cls = self.response_class(**kwargs)
        # Return the existing response record
        response_cls = session.query(
            response_cls.__class__).filter_by(**kwargs).first()
        if response_cls:
            setattr(response_cls, self.column, self.accessor(response))
            setattr(
                response_cls, self.venue_column, self.venue_accessor(response))
            kwargs.update({self.column: self.accessor(response),
                           self.venue_column: self.venue_accessor(response)})
            self._validate_and_commit(response_cls, session.add, **kwargs)
