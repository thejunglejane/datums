from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import UUIDType

from base import GhostBase, ResponseClassLegacyAccessor

__all__ = ['Response', 'BooleanResponse', 'NumericResponse', 'LocationResponse',
           'MultiResponse', 'NoteResponse', 'PeopleResponse', 'TokenResponse']


class Response(GhostBase):

    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    report_id = Column(UUIDType, ForeignKey('reports.id'))
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __str__(self):
        attrs = ['id', 'report_id', 'question_id', 'type']
        super(Response, self).__str__(attrs)


class BooleanResponse(Response):

    boolean_response = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'boolean',
    }


class LocationResponse(Response):

    location_response = Column(String)
    venue_id = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'location',
    }


class MultiResponse(Response):

    multi_response = Column(postgresql.ARRAY(String))

    __mapper_args__ = {
        'polymorphic_identity': 'multi',
    }


class NoteResponse(Response):

    note_response = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'note',
    }


class NumericResponse(Response):

    numeric_response = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'numeric',
    }


class PeopleResponse(Response):

    people_response = Column(postgresql.ARRAY(String))

    __mapper_args__ = {
        'polymorphic_identity': 'people',
    }


class TokenResponse(Response):

    tokens_response = Column(postgresql.ARRAY(String))

    __mapper_args__ = {
        'polymorphic_identity': 'tokens',
    }
