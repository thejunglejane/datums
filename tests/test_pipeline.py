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
from datums.pipeline import mappers
from sqlalchemy.orm import query


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.snapshot = {
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
        self.question = {'questionType': 'numeric',
                         'prompt': 'How anxious are you?'}
        self.report = self.snapshot.copy()
        self.responses = self.report.pop('responses')

    def tearDown(self):
        del self.snapshot
        del self.question
        del self.report
        del self.responses


class TestPipelineAdd(TestPipeline):

    def test_prepare_snapshot_photoset(self):
        '''Does _prepare_snapshot() return the report and responses contained
        in a snapshot separately as well as the photoset?
        '''
        self.snapshot['photoSet'] = []
        report, response, photoset = pipeline._prepare_snapshot(self.snapshot)
        self.assertDictEqual(report, self.report)
        self.assertEqual(response, self.responses)
        self.assertEqual(photoset, [])

    def test_prepare_snapshot_no_photoset(self):
        '''Does _prepare_snapshot() return the report without any response or
        photoset if there are none included in the snapshot?
        '''
        _ = self.snapshot.pop('responses')
        report, response, photoset = pipeline._prepare_snapshot(self.snapshot)
        self.assertDictEqual(report, self.report)
        self.assertIsNone(response)
        self.assertIsNone(photoset)

    @mock.patch.object(models.Question, 'get_or_create')
    def test_question_action_add(self, mock_get_create):
        '''Does _question(), call get_or_create() with the question type and
        prompt specified in the question passed when the action passed is
        models.Question.get_or_create? 
        '''
        pipeline._question(self.question, models.Question.get_or_create)
        mock_get_create.assert_called_once_with(
            **{'type': self.question['questionType'],
               'prompt': self.question['prompt']})

    @mock.patch.object(
        pipeline.codec.numeric_accessor, 'get_or_create_from_legacy_response')
    def test_response_action_add(self, mock_get_create):
        '''Does _response(), call get_or_create() with the response provided
        when the action passed is accessor.get_or_create_from_legacy_response? 
        '''
        pipeline._response(
            self.responses,
            pipeline.codec.numeric_accessor.get_or_create_from_legacy_response)
        mock_get_create.assert_called_once_with(self.responses)

    def test_traverse_report(self):
        '''Does _traverse_report() return two dictionaries containing the top
        and nested levels of the report passed?
        '''
        top, nested = pipeline._traverse_report(self.report, 'get_or_create')
        self.assertDictEqual(top, {
            'battery': 0.8, 'created_at': datetime.datetime(
                2015, 3, 22, 9, 10, 35, tzinfo=tzoffset(None, -14400)),
            'steps': 100, 'connection': 0, 'draft': False, 'background': 0,
            'report_impetus': 4, 'section_identifier': '1-2016-1-14',
            'id': uuid.UUID('f2b8805c-b107-462d-b6ff-d67532ef797b')})
        self.assertDictEqual(nested, {
            'weather': self.report['weather'],
            'audio': self.report['audio']})
        top, nested = pipeline._traverse_report(
            self.report['audio'], 'get_or_create',
            mappers._report_key_mapper['audio'])
        self.assertDictEqual(top, {
            'report_id': uuid.UUID(
                'f2b8805c-b107-462d-b6ff-d67532ef797b'), 'average': 5,
            'id': uuid.UUID(
                '212cd61d-faf4-4a43-b52a-be5463b0b035'), 'peak': 10})
        self.assertDictEqual(nested, {})
        top, nested = pipeline._traverse_report(
            self.report['weather'], 'get_or_create',
            mappers._report_key_mapper['weather'])
        self.assertDictEqual(top, {
            'wind_direction': 'NNW', 'weather': 'clear', 'id': uuid.UUID(
                '4c0bb156-1176-47d9-bba9-cc7950ca934d'),
            'temperature_fahrenheit': 67, 'feels_like_fahrenheit': 30,
            'dewpoint_celsius': -12, 'latitude': 40.7, 'precipitation_in': 0,
            'wind_mph': 3.4, 'wind_gust_kph': 7.9, 'precipitation_mm': 0,
            'station_id': 'KNYNEWYO118', 'temperature_celsius': 50,
            'visibility_km': 16.1, 'visibility_mi': 10, 'report_id': uuid.UUID(
                'f2b8805c-b107-462d-b6ff-d67532ef797b'), 'wind_degrees': 325,
            'wind_kph': 5.5, 'wind_gust_mph': 4.9, 'uv': 1, 'longitude': -71.1,
            'relative_humidity': '38%', 'feels_like_celsius': -1})
        self.assertDictEqual(nested, {})

    @mock.patch.object(models.Report, 'get_or_create')
    @mock.patch.object(pipeline, '_traverse_report')
    def test_report_add(self, mock_traverse_report, mock_get_create):
        '''Does _report_add() call _traverse_report() with the report provided
        with the action get_or_create()?
        '''
        mock_traverse_report.return_value = ({'foo': 'bar'}, {})
        pipeline._report_add(self.report, models.Report)
        mock_traverse_report.assert_called_once_with(
            self.report, 'get_or_create', mappers._report_key_mapper)
        mock_get_create.assert_called_once_with(**{'foo': 'bar'})

    @mock.patch.object(pipeline, '_question')
    def test_add_question(self, mock_question):
        '''Does add_question(), call _question() with the question when the
        action provided is models.Question.get_or_create?
        '''
        pipeline.add_question(self.question)
        mock_question.assert_called_once_with(
            self.question, models.Question.get_or_create)

    @mock.patch.object(pipeline.codec, 'get_response_accessor')
    @mock.patch.object(pipeline, '_response')
    @mock.patch.object(pipeline, '_report_add')
    def test_add_snapshot(
            self, mock_add_report, mock_add_response, mock_get_accessor):
        '''Does add_snapshot() call _report_add() with the report included in
        the snapshot, then call get_response_accessor() with the response and
        report included in the snapshot, and finally call _response with the
        response included in the snapshot with the action
        numeric_accessor.get_or_create_from_legacy_response?
        '''
        mock_get_accessor.return_value = (
            pipeline.codec.numeric_accessor,
            {'question_id': 1, 'report_id': self.report['uniqueIdentifier']})
        pipeline.add_snapshot(self.snapshot)
        mock_add_report.assert_called_once_with(self.report)
        mock_get_accessor.assert_called_once_with(
            self.responses[0], self.report)
        mock_add_response.assert_called_once_with(
            self.responses[0],
            pipeline.codec.numeric_accessor.get_or_create_from_legacy_response,
            **{'question_id': 1, 'report_id': self.report['uniqueIdentifier']})


class TestPipelineUpdate(TestPipeline):

    @mock.patch.object(models.Question, 'update')
    def test_question_action_update(self, mock_update):
        '''Does _question(), call update() with the question type and
        prompt specified in the question passed when the action passed is
        models.Question.update? 
        '''
        pipeline._question(self.question, models.Question.update)
        mock_update.assert_called_once_with(
            **{'type': self.question['questionType'],
               'prompt': self.question['prompt']})

    @mock.patch.object(
        pipeline.codec.numeric_accessor, 'update')
    def test_response_action_update(self, update):
        '''Does _response(), call update() with the response provided when the
        action passed is accessor.update? 
        '''
        pipeline._response(self.responses,
                           pipeline.codec.numeric_accessor.update)
        update.assert_called_once_with(self.responses)

    @mock.patch.object(models.Report, 'update')
    @mock.patch.object(pipeline, '_traverse_report')
    def test_report_update(self, mock_traverse_report, mock_update):
        '''Does _report_update(), call _traverse_report() with the report
        provided with the action update() of nested reports within the report
        provided?
        '''
        mock_traverse_report.return_value = ({'foo': 'bar'}, {})
        pipeline._report_update(self.report, models.Report)
        mock_traverse_report.assert_called_once_with(
            self.report, 'update', mappers._report_key_mapper)
        mock_update.assert_called_once_with(**{'foo': 'bar'})

    @mock.patch.object(pipeline, '_question')
    def test_update_question(self, mock_question):
        '''Does update_question(), call _question() with the question when the
        action provided is models.Question.update?
        '''
        pipeline.update_question(self.question)
        mock_question.assert_called_once_with(
            self.question, models.Question.update)

    @mock.patch.object(pipeline.codec, 'get_response_accessor')
    @mock.patch.object(pipeline, '_response')
    @mock.patch.object(pipeline, '_report_update')
    def test_update_snapshot(
            self, mock_update_report, mock_update_response, mock_get_accessor):
        '''Does update_snapshot() call _report_update() with the report included
        in the snapshot, then call get_response_accessor() with the response and
        report included in the snapshot, and finally call _response with the
        response included in the snapshot with the action
        numeric_accessor.get_or_create_from_legacy_response?
        '''
        mock_get_accessor.return_value = (
            pipeline.codec.numeric_accessor,
            {'question_id': 1, 'report_id': self.report['uniqueIdentifier']})
        pipeline.update_snapshot(self.snapshot)
        mock_update_report.assert_called_once_with(self.report)
        mock_get_accessor.assert_called_once_with(
            self.responses[0], self.report)
        mock_update_response.assert_called_once_with(
            self.responses[0], pipeline.codec.numeric_accessor.update,
            **{'question_id': 1, 'report_id': self.report['uniqueIdentifier']})


class TestPipelineDelete(TestPipeline):

    @mock.patch.object(models.Question, 'delete')
    def test_question_action_delete(self, mock_delete):
        '''Does _question(), call delete() with the question type and
        prompt specified in the question passed when the action passed is
        models.Question.delete? 
        '''
        pipeline._question(self.question, models.Question.delete)
        mock_delete.assert_called_once_with(
            **{'type': self.question['questionType'],
               'prompt': self.question['prompt']})

    @mock.patch.object(
        pipeline.codec.numeric_accessor, 'delete')
    def test_response_action_delete(self, delete):
        '''Does _response(), call delete() with the response provided when the
        action passed is accessor.delete? 
        '''
        pipeline._response(self.responses,
                           pipeline.codec.numeric_accessor.delete)
        delete.assert_called_once_with(self.responses)

    @mock.patch.object(pipeline, '_question')
    def test_delete_question(self, mock_question):
        '''Does delete_question(), call _question() with the question when the
        action provided is models.Question.delete?
        '''
        pipeline.delete_question(self.question)
        mock_question.assert_called_once_with(
            self.question, models.Question.delete)

    @mock.patch.object(models.Report, 'delete')
    def test_delete_snapshot(self, mock_delete_report):
        '''Does delete_snapshot() call _report() with the report included in
        the snapshot with the action models.Report.delete, then call 
        get_response_accessor() with the response and report included in the
        snapshot, and finally call _response with the response included in the
        snapshot with the action numeric_accessor.delete?
        '''
        pipeline.delete_snapshot(self.snapshot)
        mock_delete_report.assert_called_once_with(**{
            'id': uuid.UUID(self.report['uniqueIdentifier'])})
