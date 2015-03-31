from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship, backref

from datums.models import Base, metadata

__all__ = ['Response', 'NumericResponse', 'BooleanResponse', 'TokenResponse',
           'PeopleResponse', 'MultiResponse', 'LocationResponse']


class Response(Base):

    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    snapshot_id = Column(String, ForeignKey('snapshots.id'), primary_key=True)
    question_id = Column(String, ForeignKey('questions.id'))

    question = relationship(
        'Question', backref=backref('responses'))

    __mapper_args__ = {
        'polymorphic_identity': 'response',
        'polymorphic_on': question_prompt
    }

    def __repr__(self):
        return '''<Response(question_prompt='%s', response='%s')>''' % (
            self.question_prompt, self.response)


class NumericResponse(Base):

    __tablename__ = 'numeric_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    response = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'numeric',
    }

    def __repr__(self):
        return '''<NumericResponse(response='%s')>''' % (self.response)


class BooleanResponse(Base):

    __tablename__ = 'boolean_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    response = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'boolean',
    }

    def __repr__(self):
        return '''<BooleanResponse(response='%s')>''' % (self.response)


class TokenResponse(Base):

    __tablename__ = 'token_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    response = Column(postgresql.ARRAY(String))

    __mapper_args__ = {
        'polymorphic_identity': 'tokens',
    }

    def __repr__(self):
        return '''<TokenResponse(response='%s')>''' % (self.response)


class PeopleResponse(Base):

    __tablename__ = 'people_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    response = Column(postgresql.ARRAY(String))

    __mapper_args__ = {
        'polymorphic_identity': 'people',
    }

    def __repr__(self):
        return '''<PeopleResponse(response='%s')>''' % (self.response)


class MultiResponse(Base):

    __tablename__ = 'multi_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    response = Column(postgresql.ARRAY(String))

    __mapper_args__ = {
        'polymorphic_identity': 'multi',
    }

    def __repr__(self):
        return '''<MultiResponse(response='%s')>''' % (self.response)


class LocationResponse(Base):

    __tablename__ = 'location_responses'

    id = Column(Integer, ForeignKey('responses.id'), primary_key=True)
    response = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'location',
    }

    def __repr__(self):
        return '''<LocationResponse(response='%s')>''' % (self.response)