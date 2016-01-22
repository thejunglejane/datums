# -*- coding: utf-8 -*-

import datetime
import mock
import random
import unittest
import uuid
import warnings
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
        '''Does the update() method on QuestionPipeline objects call
        models.Question.update with the question_dict attribute?
        '''
        pipeline.QuestionPipeline(self.question).update()
        mock_update.assert_called_once_with(**self.question_dict)

    @mock.patch.object(models.Question, 'delete')
    def test_question_pipeline_delete(self, mock_delete):
        '''Does the delete() method on QuestionPipeline objects call
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
        '''Does the update() method on ResponsePipeline objects call
        codec.numeric_accessor.update with the reponse and the ids attribute?
        '''
        pipeline.ResponsePipeline(self.response, self.report).update()
        mock_update.assert_called_once_with(self.response, **self.ids)

    @mock.patch.object(codec.numeric_accessor, 'delete')
    def test_response_pipeline_delete(self, mock_delete):
        '''Does the delete() method on ResponsePipeline objects call
        codec.numeric_accessor.delete with the reponse and the ids attribute?
        '''
        pipeline.ResponsePipeline(self.response, self.report).delete()
        mock_delete.assert_called_once_with(self.response, **self.ids)


class TestReportPipeline(unittest.TestCase):

    def setUp(self):
        self.report = {'uniqueIdentifier': uuid.uuid4(), 'audio': {
            'uniqueIdentifier': uuid.uuid4(), 'avg': -59.8, 'peak': -57, },
            'connection': 0, 'battery': 0.89, 'location': {
            'uniqueIdentifier': uuid.uuid4(), 'speed': -1, 'longitude': -73.9,
            'latitude': 40.8, 'altitude': 11.2, 'placemark': {
                'uniqueIdentifier': uuid.uuid4(), 'country': 'United States',
                'locality': 'New York'}}}
        self.maxDiff = None

    def tearDown(self):
        delattr(self, 'report')

    def test_report_pipeline_init(self):
        '''Are ReportPipeline objects fully initialized?
        '''
        r = pipeline.ReportPipeline(self.report)
        self.assertTrue(hasattr(r, 'report'))
        self.assertDictEqual(r.report, self.report)

    def test_report_pipeline_report_add(self):
        '''Does the _report() method on ReportPipeline objects return a
        dictionary of top-level report attributes mapped to the correct datums
        attribute names, and an unmapped dictionary of nested report attributes
        with the parent level report's uniqueIdentifier added, when the action
        specified is models.Report.get_or_create?
        '''
        top_level, nested_level = pipeline.ReportPipeline(self.report)._report(
            models.Report.get_or_create)
        self.assertDictEqual(top_level, {
            'id': self.report['uniqueIdentifier'], 'connection': 0,
            'battery': 0.89})
        self.assertDictEqual(nested_level, {'audio': {
            'reportUniqueIdentifier': self.report['uniqueIdentifier'],
            'uniqueIdentifier': self.report['audio']['uniqueIdentifier'],
            'avg': -59.8, 'peak': -57}, 'location': {
                'reportUniqueIdentifier': self.report['uniqueIdentifier'],
                'uniqueIdentifier': self.report['location']['uniqueIdentifier'],
                'latitude': 40.8, 'longitude': -73.9, 'altitude': 11.2,
                'speed': -1, 'placemark': {
                    'uniqueIdentifier': self.report['location'][
                        'placemark']['uniqueIdentifier'],
                    'country': 'United States', 'locality': 'New York'}}})

    def test_report_pipeline_report_add_altitude_no_uuid(self):
        '''Does the _report() method on ReportPipeline objects add a
        uniqueIdentifier to a nested AltitudeReport if there isn't one and the
        action specified is models.Report.get_or_create?
        '''
        self.report['altitude'] = {
            'floorsDescended': 0, 'pressure': 101.5, 'floorsAscended': 0}
        top_level, nested_level = pipeline.ReportPipeline(self.report)._report(
            models.Report.get_or_create)
        self.assertSetEqual(set(nested_level['altitude'].keys()),
                            set(['uniqueIdentifier', 'floorsAscended',
                                 'floorsDescended', 'pressure',
                                 'reportUniqueIdentifier']))

    def test_report_pipeline_report_attr_not_supported(self):
        '''Does the _report() method on ReportPipeline objects generate a
        warning if there is an attribute in the report that is not yet
        supported (i.e., not yet in mappers._report_key_mapper)?
        '''
        r = {'foo': 'bar'}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            pipeline.ReportPipeline(r)._report(models.Report.get_or_create)
            self.assertEquals(len(w), 1)
            self.assertEquals(w[-1].category, UserWarning)

    def test_report_pipeline_report_update_altitude_no_uuid(self):
        '''Does the _report() method on ReportPipeline objects NOT add a
        uniqueIdentifier to a nested AltitudeReport and generate a warning if
        there isn't one and the action specified is models.Report.update?
        '''
        self.report['altitude'] = {
            'floorsDescended': 0, 'pressure': 101.5, 'floorsAscended': 0}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            top_level, nested_level = pipeline.ReportPipeline(
                self.report)._report(models.Report.update)
            self.assertEquals(len(w), 1)
            self.assertEquals(w[-1].category, UserWarning)
            self.assertSetEqual(
                set(nested_level.keys()), set(['audio', 'location']))

    def test_report_pipeline_report_update_altitude_uuid(self):
        '''Does the _report() method on ReportPipeline objects NOT generate a
        warning if there is a nested AltitudeReport has a uniqueIdentifier and
        the action specified is models.Report.update?
        '''
        self.report['altitude'] = {
            'floorsDescended': 0, 'pressure': 101.5,
            'floorsAscended': 0, 'uniqueIdentifier': uuid.uuid4()}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            top_level, nested_level = pipeline.ReportPipeline(
                self.report)._report(models.Report.update)
            self.assertEquals(len(w), 0)
            self.assertSetEqual(set(nested_level.keys()),
                                set(['audio', 'location', 'altitude']))

    # TODO (jsa): test recursion
    @mock.patch.object(models.Report, 'get_or_create')
    @mock.patch.object(pipeline.ReportPipeline, '_report')
    def test_report_pipeline_add(self, mock_report, mock_get_create):
        '''Does the add() method on ReportPipeline objects call the _report()
        method on the object and then call models.Report.get_or_create() with
        the top level dictionary returned, then recurse the keys in the nested
        dictionary returned?
        '''
        top_level = {'id': uuid.uuid4()}
        mock_report.return_value = (top_level, {})
        pipeline.ReportPipeline(self.report).add(models.Report.get_or_create)
        mock_report.assert_called_once_with(
            mock_get_create, mappers._report_key_mapper)
        mock_get_create.assert_called_once_with(**top_level)

    # TODO (jsa): test recursion
    @mock.patch.object(models.Report, 'update')
    @mock.patch.object(pipeline.ReportPipeline, '_report')
    def test_report_pipeline_update(self, mock_report, mock_update):
        '''Does the update() method on ReportPipeline objects call the _report()
        method on the object and then call models.Report.update() with the top
        level dictionary returned, then recurse the keys in the nested
        dictionary returned?
        '''
        top_level = {'id': uuid.uuid4()}
        mock_report.return_value = (top_level, {})
        pipeline.ReportPipeline(self.report).update(models.Report.update)
        mock_report.assert_called_once_with(
            mock_update, mappers._report_key_mapper)
        mock_update.assert_called_once_with(**top_level)

    @mock.patch.object(models.Report, 'delete')
    def test_report_pipeline_delete(self, mock_report_delete):
        '''Does the delete() method on ReportPipeline objects call the
        models.Report.delete() method with the uniqueIdentifier of the report?
        '''
        pipeline.ReportPipeline(self.report).delete()
        mock_report_delete.assert_called_once_with(
            **{'id': self.report['uniqueIdentifier']})


class TestSnapshotPipeline(unittest.TestCase):

    def setUp(self):
        self.snapshot = {'uniqueIdentifier': uuid.uuid4(), 'responses': [
            {'questionPrompt': 'How tired are you?',
             'uniqueIdentifier': uuid.uuid4(), 'numericResponse': '2'},
            {'questionPrompt': 'Where are you?',
             'uniqueIdentifier': uuid.uuid4(),
             'locationResponse': {
                 'longitude': -73.9,
                 'latitude': 40.8,
                 'uniqueIdentifier': uuid.uuid4()}, 'text': 'Home'}]}
        self.report = self.snapshot.copy()
        self.responses = self.report.pop('responses')
        self._ = None

    def tearDown(self):
        delattr(self, 'snapshot')
        delattr(self, 'report')
        delattr(self, 'responses')
        delattr(self, '_')

    def test_snapshot_pipeline_init_no_photoset(self):
        '''Are SnapshotPipeline objects fully initialized when no photoSet is
        present?
        '''
        s = pipeline.SnapshotPipeline(self.snapshot)
        self.assertTrue(hasattr(s, 'report'))
        self.assertTrue(hasattr(s, 'responses'))
        self.assertFalse(hasattr(s, '_'))
        self.assertDictEqual(s.report, self.report)
        self.assertListEqual(s.responses, self.responses)

    def test_snapshot_pipeline_init_photoset(self):
        '''Are SnapshotPipeline objects fully initialized when a photoSet is
        present?
        '''
        self.snapshot['photoSet'] = {'photos': [
            {'uniqueIdentifier': uuid.uuid4()}]}
        s = pipeline.SnapshotPipeline(self.snapshot)
        self.assertTrue(hasattr(s, 'report'))
        self.assertTrue(hasattr(s, 'responses'))
        self.assertFalse(hasattr(s, '_'))
        self.assertDictEqual(s.report, self.report)
        self.assertListEqual(s.responses, self.responses)

    @mock.patch.object(pipeline.ResponsePipeline, 'add')
    @mock.patch.object(pipeline.ReportPipeline, 'add')
    def test_snapshot_pipeline_add(self, mock_report_add, mock_response_add):
        '''Does the add() method on SnapshotPipeline objects initialize a
        ReportPipeline object and call its add() method, and initialize n
        ResponsePipeline objects and call their add() methods, where n is the
        number of responses included in the snapshot?
        '''
        pipeline.SnapshotPipeline(self.snapshot).add()
        self.assertTrue(mock_report_add.call_count, 1)
        self.assertEquals(mock_response_add.call_count, 2)

    @mock.patch.object(pipeline.ResponsePipeline, 'update')
    @mock.patch.object(pipeline.ReportPipeline, 'update')
    def test_snapshot_pipeline_update(
            self, mock_report_update, mock_response_update):
        '''Does the update() method on SnapshotPipeline objects initialize a
        ReportPipeline object and call its update() method, and initialize n
        ResponsePipeline objects and call their update() methods, where n is
        the number of responses included in the snapshot?
        '''
        pipeline.SnapshotPipeline(self.snapshot).update()
        self.assertTrue(mock_report_update.call_count, 1)
        self.assertEquals(mock_response_update.call_count, 2)

    @mock.patch.object(pipeline.ResponsePipeline, 'delete')
    @mock.patch.object(pipeline.ReportPipeline, 'delete')
    def test_snapshot_pipeline_delete(
            self, mock_report_delete, mock_response_delete):
        '''Does the delete() method on SnapshotPipeline objects initialize a
        ReportPipeline object and call its delete() method, without initializing
        any ResponsePipeline objects and calling their delete() methods?
        '''
        pipeline.SnapshotPipeline(self.snapshot).delete()
        self.assertTrue(mock_report_delete.call_count, 1)
        mock_response_delete.assert_not_called()
