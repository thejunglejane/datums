# -*- coding: utf-8 -*-

from datums import models
from datums.pipeline import codec
from sqlalchemy.orm import query
import mock
import unittest


class TestModelsBase(unittest.TestCase):

    def setUp(self):
        self.response = {'questionPrompt': 'How anxious are you?',
                         'uniqueIdentifier': '5496B14F-EAF1-4EF7-85DB-9531FDD7DC17',
                         'numericResponse': '0'}
        self.report = {
            'uniqueIdentifier': '1B7AADBF-C137-4F35-A099-D73ACE534CFC'}

    def tearDown(self):
        del self.response
        del self.report

    def test_human_to_boolean_none(self):
        '''Does human_to_boolean return None if a non-list or an empty list is
        passed?
        '''
        self.assertIsNone(codec.human_to_boolean([]))
        self.assertIsNone(codec.human_to_boolean(3))

    def test_human_to_boolean_true(self):
        '''Does human_to_boolean return True if a list containing 'Yes' is
        passed?
        '''
        self.assertTrue(codec.human_to_boolean(['Yes']))

    def test_human_to_boolean_false(self):
        '''Does human_to_boolean return False if a list containing 'No', or
        something else that is not 'Yes', is passed?
        '''
        self.assertFalse(codec.human_to_boolean(['No']))
        self.assertFalse(codec.human_to_boolean(['Foo']))

    def test_human_to_boolean_true_followed_by_false(self):
        '''Does human_to_boolean return True if the first element of the list
        is 'Yes', ignoring other elements of the list?
        '''
        self.assertTrue(codec.human_to_boolean(['Yes', 'No']))

    @mock.patch.object(query.Query, 'first')
    @mock.patch.object(query.Query, 'filter', return_value=query.Query(
        models.Question))
    @mock.patch.object(
        models.session, 'query', return_value=query.Query(models.Question))
    def test_get_response_accessor_valid_response_type(
            self, mock_session_query, mock_query_filter, mock_query_first):
        '''Does get_response_accessor() return the right response_mapper for
        the prompt in the response, as well as the question and report ID?
        '''
        mock_query_first.return_value = (1, 5)
        mapper, ids = codec.get_response_accessor(self.response, self.report)
        mock_session_query.assert_called_once_with(
            models.Question.id, models.Question.type)
        self.assertTrue(mock_query_filter.called)
        self.assertEqual(mapper, codec.numeric_accessor)
        self.assertIsInstance(mapper, models.base.ResponseClassLegacyAccessor)
        self.assertDictEqual(ids, {
            'question_id': 1, 'report_id': self.report['uniqueIdentifier']})
