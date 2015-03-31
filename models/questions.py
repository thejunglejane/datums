from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String

from datums.models import Base, metadata

__all__ = ['Question']


class Question(Base):

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    prompt = Column(String)

    def __repr__(self):
        return '''<Question(prompt='%s')>''' % (self.prompt)
