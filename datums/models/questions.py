# -*- coding: utf-8 -*-

from base import GhostBase, session
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship


__all__ = ['Question']


class Question(GhostBase):

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, unique=True)
    type = Column(Integer, nullable=False)  # questionType
    prompt = Column(String, nullable=False)  # questionPrompt

    responses = relationship('Response', cascade='save-update, merge, delete')

    def __str__(self):
        attrs = ['id', 'type', 'prompt']
        super(Question, self).__str__(attrs)
