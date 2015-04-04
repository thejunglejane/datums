from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.dialects import postgresql

# from datums.models import Base, metadata

__all__ = ['Response', 'BooleanResponse', 'NumericResponse', 'LocationResponse',
           'MultiResponse', 'NoteResponse', 'PeopleResponse', 'TokenResponse']


class Response(Base):

    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __repr__(self):
        return '''<Response(type='%s'>''' % (self.type)


class BooleanResponse(Base):

    __tablename__ = 'boolean_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    response = Column(Boolean)  # answeredOptions

    __mapper_args__ = {
        'polymorphic_identity': 'boolean',
    }

    def __repr__(self):
        return '''<BooleanResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)


class LocationResponse(Base):

    __tablename__ = 'location_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    response = Column(String)  # text
    venue_id = Column(String)  # foursquareVenueId

    __mapper_args__ = {
        'polymorphic_identity': 'location',
    }

    def __repr__(self):
        return '''<LocationResponse(question_id='%s', response='%s',
            venue_id='%s')>''' % (
                self.question_id, self.response, self.venue_id)


class MultiResponse(Base):

    __tablename__ = 'multi_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    response = Column(postgresql.ARRAY(String))  # answeredOptions

    __mapper_args__ = {
        'polymorphic_identity': 'multi',
    }

    def __repr__(self):
        return '''<MultiResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)


class NoteResponse(Base):

    __tablename__ = 'note_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    response = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'note',
    }

    def __repr__(self):
        return '''<NoteResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)


class NumericResponse(Base):

    __tablename__ = 'numeric_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    response = Column(Integer)  # numericResponse

    __mapper_args__ = {
        'polymorphic_identity': 'numeric',
    }

    def __repr__(self):
        return '''<NumericResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)


class PeopleResponse(Base):

    __tablename__ = 'people_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    response = Column(postgresql.ARRAY(String))  # text

    __mapper_args__ = {
        'polymorphic_identity': 'people',
    }

    def __repr__(self):
        return '''<PeopleResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)


class TokenResponse(Base):

    __tablename__ = 'token_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    response = Column(postgresql.ARRAY(String))  # text

    __mapper_args__ = {
        'polymorphic_identity': 'tokens',
    }

    def __repr__(self):
        return '''<TokenResponse(question_id='%s', response='%s')>''' % (
            self.question_id, self.response)
