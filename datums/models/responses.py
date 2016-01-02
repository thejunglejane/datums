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
    snapshot_id = Column(UUIDType, ForeignKey('snapshots.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __repr__(self):
        return '''<{self.__name__}(
            id={self.id}, snapshot_id={self.snapshot_id},
            question_id={self.question_id}, type={self.type}
            )>'''.format(self)


class BooleanResponse(Response):

    boolean_response = Column(Boolean)  # answeredOptions

    __mapper_args__ = {
        'polymorphic_identity': 'boolean',
    }


class LocationResponse(Response):

    location_response = Column(String)  # text
    venue_id = Column(String, nullable=True)  # foursquareVenueId

    __mapper_args__ = {
        'polymorphic_identity': 'location',
    }


class MultiResponse(Response):

    multi_response = Column(postgresql.ARRAY(String))  # answeredOptions

    __mapper_args__ = {
        'polymorphic_identity': 'multi',
    }


class NoteResponse(Response):

    note_response = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'note',
    }


class NumericResponse(Response):

    numeric_response = Column(Float)  # numericResponse

    __mapper_args__ = {
        'polymorphic_identity': 'numeric',
    }


class PeopleResponse(Response):

    people_response = Column(postgresql.ARRAY(String))  # text

    __mapper_args__ = {
        'polymorphic_identity': 'people',
    }


class TokenResponse(Response):

    tokens_response = Column(postgresql.ARRAY(String))  # text

    __mapper_args__ = {
        'polymorphic_identity': 'tokens',
    }
