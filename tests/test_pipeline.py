# -*- coding: utf-8 -*-

import datetime
import mock
import random
import unittest
import uuid
from dateutil.parser import parse
from dateutil.tz import tzoffset
from datums import models
from datums import pipeline
from datums.pipeline import mappers, codec
from sqlalchemy.orm import query


class TestQuestionPipeline(unittest.TestCase):

    def setUp(self):
        self.question = {'questionType': 'numeric',
                         'prompt': 'How anxious are you?'}
        self.question_dict = {'type': self.question['questionType'],
                              'prompt': self.question['prompt']}

    def tearDown(self):
        delattr(self, 'question')
        delattr(self, 'question_dict')

    def test_question_pipeline_init(self):
        '''Are QuestionPipeline objects fully initialized?
        '''
        q = pipeline.QuestionPipeline(self.question)
        self.assertTrue(hasattr(q, 'question_dict'))
        self.assertDictEqual(q.question_dict, self.question_dict)

    @mock.patch.object(models.Question, 'get_or_create')
    def test_question_pipeline_add(self, mock_get_create):
        '''Does the add() method on QuestionPipeline objects call
        models.Question.get_or_create with the question_dict attribute?
        '''
        pipeline.QuestionPipeline(self.question).add()
        mock_get_create.assert_called_once_with(**self.question_dict)

    @mock.patch.object(models.Question, 'update')
    def test_question_pipeline_update(self, mock_update):
        '''Does the add() method on QuestionPipeline objects call
        models.Question.update with the question_dict attribute?
        '''
        pipeline.QuestionPipeline(self.question).update()
        mock_update.assert_called_once_with(**self.question_dict)

    @mock.patch.object(models.Question, 'delete')
    def test_question_pipeline_delete(self, mock_delete):
        '''Does the add() method on QuestionPipeline objects call
        models.Question.delete with the question_dict attribute?
        '''
        pipeline.QuestionPipeline(self.question).delete()
        mock_delete.assert_called_once_with(**self.question_dict)


class TestResponsePipeline(unittest.TestCase):

    def setUp(self):
        self.report = {'uniqueIdentifier': uuid.uuid4(), 'responses': [{
            'questionPrompt': 'How anxious are you?',
            'uniqueIdentifier': uuid.uuid4(),
            'numericResponse': '1'}]}
        self.response = self.report.pop('responses')[0]
        self.accessor = codec.numeric_accessor
        self.ids = {'report_id': self.report['uniqueIdentifier'],
                    'question_id': 1}

    def tearDown(self):
        delattr(self, 'report')
        delattr(self, 'response')
        delattr(self, 'accessor')
        delattr(self, 'ids')

    def test_response_pipeline_init(self):
        '''Are ResponsePipeline objects fully initialized?
        '''
        r = pipeline.ResponsePipeline(self.response, self.report)
        self.assertTrue(hasattr(r, 'accessor'))
        self.assertTrue(hasattr(r, 'ids'))
        self.assertEquals(r.accessor, self.accessor)
        self.assertDictEqual(r.ids, self.ids)

    @mock.patch.object(
        codec.numeric_accessor, 'get_or_create_from_legacy_response')
    def test_response_pipeline_add(self, mock_get_create_legacy):
        '''Does the add() method on ResponsePipeline objects call
        codec.numeric_accessor.get_or_create_from_legacy_response with the
        reponse and the ids attribute?
        '''
        pipeline.ResponsePipeline(self.response, self.report).add()
        mock_get_create_legacy.assert_called_once_with(
            self.response, **self.ids)

    @mock.patch.object(codec.numeric_accessor, 'update')
    def test_response_pipeline_update(self, mock_update):
        '''Does the add() method on ResponsePipeline objects call
        codec.numeric_accessor.update with the reponse and the ids attribute?
        '''
        pipeline.ResponsePipeline(self.response, self.report).update()
        mock_update.assert_called_once_with(self.response, **self.ids)

    @mock.patch.object(codec.numeric_accessor, 'delete')
    def test_response_pipeline_delete(self, mock_delete):
        '''Does the add() method on ResponsePipeline objects call
        codec.numeric_accessor.delete with the reponse and the ids attribute?
        '''
        pipeline.ResponsePipeline(self.response, self.report).delete()
        mock_delete.assert_called_once_with(self.response, **self.ids)


class TestSnapshotPipeline(unittest.TestCase):

    def setUp(self):
        self.snapshot = {}
        self.report = self.snapshot.copy()
        self.responses = self.report.pop('responses')
        self._ = None

    def tearDown(self):
        delattr(self, 'snapshot')
        delattr(self, 'report')
        delattr(self, 'responses')
        delattr(self, '_')

    def test_snapshot_pipeline_init(self):
        pass

    def test_snapshot_pipeline_add(self):
        pass

    def test_snapshot_pipeline_update(self):
        pass

    def test_snapshot_pipeline_delete(self):
        pass
