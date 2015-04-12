from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from base import GhostBase, session

__all__ = ['Question']


class Question(GhostBase):

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, unique=True)
    type = Column(Integer, nullable=False)  # questionType
    prompt = Column(String, nullable=False)  # questionPrompt

    responses = relationship('Response', cascade='save-update, merge, delete')

    def __repr__(self):
        return '''<Question(type='%s', prompt='%s')>''' % (self.type,
                                                           self.prompt)
