from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String

from base import GhostBase, session

__all__ = ['Question']


class Question(GhostBase):

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, unique=True)
    type = Column(Integer)  # questionType
    prompt = Column(String)  # questionPrompt

    def __repr__(self):
        return '''<Question(type='%s', prompt='%s')>''' % (self.type,
                                                           self.prompt)
