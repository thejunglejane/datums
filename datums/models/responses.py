from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import UUIDType

from base import GhostBase

__all__ = ['Response', 'BooleanResponse', 'NumericResponse', 'LocationResponse',
           'MultiResponse', 'NoteResponse', 'PeopleResponse', 'TokenResponse']


class Response(GhostBase):

    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    snapshot_id = Column(UUIDType, ForeignKey('snapshots.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    type = Column(String)

    question = relationship(
        'Question', backref=backref('responses', order_by=id))

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __repr__(self):
        return '''<Response(type='%s'>''' % (self.type)


class BooleanResponse(Response):

    boolean_response = Column(Boolean)  # answeredOptions

    __mapper_args__ = {
        'polymorphic_identity': 'boolean',
    }

    def __repr__(self):
        return '''<BooleanResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)


class LocationResponse(Response):

    location_response = Column(String)  # text
    venue_id = Column(String, nullable=True)  # foursquareVenueId

    __mapper_args__ = {
        'polymorphic_identity': 'location',
    }

    def __repr__(self):
        return '''<LocationResponse(question_id='%s', response='%s',
            venue_id='%s')>''' % (
            self.question_id, self.response, self.venue_id)


class MultiResponse(Response):

    multi_response = Column(postgresql.ARRAY(String))  # answeredOptions

    __mapper_args__ = {
        'polymorphic_identity': 'multi',
    }

    def __repr__(self):
        return '''<MultiResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)


class NoteResponse(Response):

    note_response = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'note',
    }

    def __repr__(self):
        return '''<NoteResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)


class NumericResponse(Response):

    numeric_response = Column(Integer)  # numericResponse

    __mapper_args__ = {
        'polymorphic_identity': 'numeric',
    }

    def __repr__(self):
        return '''<NumericResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)


class PeopleResponse(Response):

    people_response = Column(postgresql.ARRAY(String))  # text

    __mapper_args__ = {
        'polymorphic_identity': 'people',
    }

    def __repr__(self):
        return '''<PeopleResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)


class TokenResponse(Response):

    tokens_response = Column(postgresql.ARRAY(String))  # text

    __mapper_args__ = {
        'polymorphic_identity': 'tokens',
    }

    def __repr__(self):
        return '''<TokenResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)
