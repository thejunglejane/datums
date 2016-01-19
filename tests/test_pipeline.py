# -*- coding: utf-8 -*-

import mock
import random
import unittest
import uuid
from dateutil.parser import parse
from datums import models
from datums.pipeline import add, codec, delete, mappers, update
from sqlalchemy.orm import query


# TODO (jsa): diversify tests
class TestPipelineAdd(unittest.TestCase):

    _response_classes = models.Response.__subclasses__()

    def setUp(self):
        self.report = {
            'uniqueIdentifier': 'f2b8805c-b107-462d-b6ff-d67532ef797b',
            'date': '2015-03-22T09:10:35-0400', 'reportImpetus': 4,
            'battery': 0.80, 'steps': 100, 'sectionIdentifier': '1-2016-1-14',
            'background': 0, 'connection': 0, 'draft': 0,
            'audio': {
                'uniqueIdentifier': '212cd61d-faf4-4a43-b52a-be5463b0b035',
                'avg': 5, 'peak': 10
            },
            'weather': {
                'uniqueIdentifier': '4c0bb156-1176-47d9-bba9-cc7950ca934d',
                'stationID': 'KNYNEWYO118', 'latitude': 40.7,
                'longitude': -71.1, 'weather': 'clear', 'tempF': 67,
                'tempC': 50, 'feelslikeF': 30, 'feelslikeC': -1,
                'windDirection': 'NNW', 'windDegrees': 325, 'windMPH': 3.4,
                'windKPH': 5.5, 'windGustMPH': 4.9, 'windGustKPH': 7.9,
                'relativeHumidity': '38%', 'precipTodayIn': 0,
                'precipTodayMetric': 0, 'dewpointC': -12, 'visibilityMi': 10,
                'visibilityKM': 16.1, 'uv': 1
            },
            'responses': [
                {'questionPrompt': 'How anxious are you?',
                 'uniqueIdentifier': 'B47C8530-BDFF-441A-AD82-36CD01B2DC6C',
                 'numericResponse': '1'}]
        }
        self.response = self.report['responses'][0]
        self.question = {'questionType': 'numeric',
                         'prompt': 'How anxious are you?'}

    def tearDown(self):
        del self.report
        del self.response
        del self.question

    @mock.patch.object(models.Question, 'get_or_create')
    def test_add_question(self, mock_get_create):
        '''Does add_question() call get_or_create() with the question type and
        prompt specified in the question passed? 
        '''
        add.add_question(question=self.question)
        mock_get_create.assert_called_once_with(
            **{'type': self.question['questionType'],
               'prompt': self.question['prompt']})

    @mock.patch.object(add, '_add_response')
    @mock.patch.object(add, '_add_report')
    def test_add_snapshot(self, mock_add_report, mock_add_response):
        '''Does add_snapshot add the report and response(s) included in the
        snapshot provided?
        '''
        # Simulate popping of 'responses' attribute from snapshot
        _ = {key: value for key, value in self.report.iteritems()
            if key != 'responses'}
        add.add_snapshot(self.report)
        mock_add_report.assert_called_once_with(_, 'report')
        mock_add_response.assert_called_once_with(self.response, _)

    @mock.patch.object(models.base.ResponseClassLegacyAccessor,
                       'get_or_create_from_legacy_response')
    @mock.patch.object(codec, 'get_response_accessor')
    def test_add_response(self, mock_get_accessor, mock_get_response):
        '''Does _add_response() call get_reponse_accessor() and
        get_or_create_from_legacy_response()?
        '''
        _accessor = models.base.ResponseClassLegacyAccessor(
            response_class=random.choice(self._response_classes),
            column='foo_response', accessor=(lambda x: x.get('foo')))
        _ids = {'foo': 'bar'}
        mock_get_accessor.return_value = _accessor, _ids
        add._add_response(self.response, self.report)
        mock_get_accessor.assert_called_once_with(self.response, self.report)
        mock_get_response.assert_called_once_with(self.response, **_ids)

    @mock.patch.object(models.AudioReport, 'get_or_create')
    def test_add_report(self, mock_get_create):
        '''Does _add_report() call get_or_create() with the report info in
        the report passed, and recurse nested reports within the report? 
        '''
        self.report['audio']['reportUniqueIdentifier'] = uuid.UUID(
            self.report['uniqueIdentifier'])
        add._add_report(
            self.report['audio'], 'audio', mappers._report_key_mapper['audio'])
        mock_get_create.assert_called_once_with(
            **{'average': 5, 'id': uuid.UUID(
                self.report['audio']['uniqueIdentifier']), 'peak': 10,
               'report_id': uuid.UUID(self.report['uniqueIdentifier'])})


class TestPipelineUpdate(unittest.TestCase):

    _response_classes = models.Response.__subclasses__()

    def setUp(self):
        self.report = {
            'uniqueIdentifier': 'f2b8805c-b107-462d-b6ff-d67532ef797b',
            'date': '2015-03-22T09:10:35-0400', 'reportImpetus': 4,
            'battery': 0.80, 'steps': 100, 'sectionIdentifier': '1-2016-1-14',
            'background': 0, 'connection': 0, 'draft': 0,
            'audio': {
                'uniqueIdentifier': '212cd61d-faf4-4a43-b52a-be5463b0b035',
                'avg': 5, 'peak': 10
            },
            'weather': {
                'uniqueIdentifier': '4c0bb156-1176-47d9-bba9-cc7950ca934d',
                'stationID': 'KNYNEWYO118', 'latitude': 40.7,
                'longitude': -71.1, 'weather': 'clear', 'tempF': 67,
                'tempC': 50, 'feelslikeF': 30, 'feelslikeC': -1,
                'windDirection': 'NNW', 'windDegrees': 325, 'windMPH': 3.4,
                'windKPH': 5.5, 'windGustMPH': 4.9, 'windGustKPH': 7.9,
                'relativeHumidity': '38%', 'precipTodayIn': 0,
                'precipTodayMetric': 0, 'dewpointC': -12, 'visibilityMi': 10,
                'visibilityKM': 16.1, 'uv': 1
            },
            'responses': [
                {'questionPrompt': 'How anxious are you?',
                 'uniqueIdentifier': 'B47C8530-BDFF-441A-AD82-36CD01B2DC6C',
                 'numericResponse': '1'}]
        }
        self.response = self.report['responses'][0]
        self.question = {'questionType': 'numeric',
                         'prompt': 'How anxious are you?'}

    def tearDown(self):
        del self.report
        del self.response
        del self.question

    @mock.patch.object(models.Question, 'update')
    def test_update_question(self, mock_update):
        '''Does update_question() call update() with the question type and
        prompt specified in the question passed? 
        '''
        update.update_question(question=self.question)
        mock_update.assert_called_once_with(self.question, **{
            'type': self.question['questionType'],
            'prompt': self.question['prompt']})

    @mock.patch.object(update, '_update_response')
    @mock.patch.object(update, '_update_report')
    def test_update_snapshot(self, mock_update_report, mock_update_response):
        '''Does update_snapshot update the report and response(s) included in
        the snapshot provided?
        '''
        # Simulate popping of 'responses' attribute from snapshot
        _ = {key: value for key, value in self.report.iteritems()
            if key != 'responses'}
        update.update_snapshot(self.report)
        mock_update_report.assert_called_once_with(_, 'report')
        mock_update_response.assert_called_once_with(self.response, _)

    @mock.patch.object(models.base.ResponseClassLegacyAccessor, 'update')
    @mock.patch.object(codec, 'get_response_accessor')
    def test_update_response(self, mock_get_accessor, mock_update):
        '''Does _update_response() call get_reponse_accessor() and
        update()?
        '''
        _accessor = models.base.ResponseClassLegacyAccessor(
            response_class=random.choice(self._response_classes),
            column='foo_response', accessor=(lambda x: x.get('foo')))
        _ids = {'foo': 'bar'}
        mock_get_accessor.return_value = _accessor, _ids
        update._update_response(self.response, self.report)
        mock_get_accessor.assert_called_once_with(self.response, self.report)
        mock_update.assert_called_once_with(self.response, **_ids)

    @mock.patch.object(models.AudioReport, 'update')
    def test_update_report(self, mock_update):
        '''Does _update_report() call update() with the report info in the
        report passed, and recurse nested reports within the report? 
        '''
        self.report['audio']['reportUniqueIdentifier'] = uuid.UUID(
            self.report['uniqueIdentifier'])
        update._update_report(
            self.report['audio'], 'audio', mappers._report_key_mapper['audio'])
        mock_update.assert_called_once_with(self.report['audio'], **{
            'average': 5, 'id': uuid.UUID(
                self.report['audio']['uniqueIdentifier']),
            'peak': 10, 'report_id': uuid.UUID(
                self.report['uniqueIdentifier'])})


class TestPipelineDelete(unittest.TestCase):

    _response_classes = models.Response.__subclasses__()

    def setUp(self):
        self.report = {
            'uniqueIdentifier': 'f2b8805c-b107-462d-b6ff-d67532ef797b',
            'date': '2015-03-22T09:10:35-0400', 'reportImpetus': 4,
            'battery': 0.80, 'steps': 100, 'sectionIdentifier': '1-2016-1-14',
            'background': 0, 'connection': 0, 'draft': 0,
            'audio': {
                'uniqueIdentifier': '212cd61d-faf4-4a43-b52a-be5463b0b035',
                'avg': 5, 'peak': 10
            },
            'weather': {
                'uniqueIdentifier': '4c0bb156-1176-47d9-bba9-cc7950ca934d',
                'stationID': 'KNYNEWYO118', 'latitude': 40.7,
                'longitude': -71.1, 'weather': 'clear', 'tempF': 67,
                'tempC': 50, 'feelslikeF': 30, 'feelslikeC': -1,
                'windDirection': 'NNW', 'windDegrees': 325, 'windMPH': 3.4,
                'windKPH': 5.5, 'windGustMPH': 4.9, 'windGustKPH': 7.9,
                'relativeHumidity': '38%', 'precipTodayIn': 0,
                'precipTodayMetric': 0, 'dewpointC': -12, 'visibilityMi': 10,
                'visibilityKM': 16.1, 'uv': 1
            },
            'responses': [
                {'questionPrompt': 'How anxious are you?',
                 'uniqueIdentifier': 'B47C8530-BDFF-441A-AD82-36CD01B2DC6C',
                 'numericResponse': '1'}]
        }
        self.response = self.report['responses'][0]
        self.question = {'questionType': 'numeric',
                         'prompt': 'How anxious are you?'}

    def tearDown(self):
        del self.report
        del self.response
        del self.question

    @mock.patch.object(models.Question, 'delete')
    def test_delete_question(self, mock_delete):
        '''Does delete_question() call delete() with the question type and
        prompt specified in the question passed? 
        '''
        delete.delete_question(question=self.question)
        mock_delete.assert_called_once_with(**{
            'type': self.question['questionType'],
            'prompt': self.question['prompt']})

    @mock.patch.object(delete, '_delete_report')
    def test_delete_snapshot(self, mock_delete_report):
        '''Does delete_snapshot delete the report included in the snapshot
        provided?
        '''
        # Simulate popping of 'responses' attribute from snapshot
        _ = {key: value for key, value in self.report.iteritems()
            if key != 'responses'}
        delete.delete_snapshot(self.report)
        mock_delete_report.assert_called_once_with(_, 'report')

    @mock.patch.object(models.AudioReport, 'delete')
    def test_delete_report(self, mock_delete):
        '''Does _delete_report() call delete() with the report info in the
        report passed, and recurse nested reports within the report? 
        '''
        delete._delete_report(self.report, 'report', mappers._report_key_mapper)
        mock_delete.assert_called_once_with(**{
            'id': uuid.UUID(self.report['uniqueIdentifier'])})
