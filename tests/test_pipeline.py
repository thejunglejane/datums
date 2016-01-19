# -*- coding: utf-8 -*-

import mock
import random
import unittest
import uuid
from dateutil.parser import parse
from datums import models
from datums import pipeline
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
        self.response = self.report.pop('responses')

    def tearDown(self):
        del self.snapshot
        del self.question
        del self.report
        del self.response


class TestPipelineAdd(TestPipeline):

    def test_prepare_snapshot_photoset(self):
        '''Does _prepare_snapshot() return the report and responses contained
        in a snapshot separately as well as the photoset?
        '''
        self.snapshot['photoSet'] = []
        report, response, photoset = pipeline._prepare_snapshot(self.snapshot)
        self.assertDictEqual(report, self.report)
        self.assertEqual(response, self.response)
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
            self.response,
            pipeline.codec.numeric_accessor.get_or_create_from_legacy_response)
        mock_get_create.assert_called_once_with(self.response)

    @mock.patch.object(models.WeatherReport, 'get_or_create')
    @mock.patch.object(models.AudioReport, 'get_or_create')
    @mock.patch.object(models.Report, 'get_or_create')
    def test_report_action_add(
            self, mock_get_create, mock_audio_get_create,
            mock_weather_get_create):
        '''Does _report(), call get_or_create() with the report provided when
        the action passed is models.Report.get_or_create, then recursively call
        the get_or_create() of nested reports within the report provided? 
        '''
        # TODO (jsa): mock function name discovery
        pipeline._report(self.report, 'report', models.Report.get_or_create)
        mock_get_create.assert_called_once_with(
            **{k: v for k, v in self.report if not isinstance(v, dict)})
        mock_audio_get_create.assert_called_once_with(**{self.report['audio']})
        mock_weather_get_create.assert_called_once_with(
            **{self.report['weather']})

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
    @mock.patch.object(pipeline, '_report')
    def test_add_snapshot(
            self, mock_add_report, mock_add_response, mock_get_accessor):
        '''Does add_snapshot() call _report() with the report included in the
        snapshot with the action models.Report.get_or_create, then call 
        get_response_accessor() with the response and report included in the
        snapshot, and finally call _response with the response
        included in the snapshot with the action
        numeric_accessor.get_or_create_from_legacy_response?
        '''
        mock_get_accessor.return_value = (
            pipeline.codec.numeric_accessor,
            {'question_id': 1, 'report_id': self.report['uniqueIdentifier']})
        pipeline.add_snapshot(self.snapshot)
        mock_add_report.assert_called_once_with(
            self.report, 'report', models.Report.get_or_create)
        mock_get_accessor.assert_called_once_with(
            self.response[0], self.report)
        mock_add_response.assert_called_once_with(
            self.response[0],
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
        pipeline._response(self.response,
                           pipeline.codec.numeric_accessor.update)
        update.assert_called_once_with(self.response)

    @mock.patch.object(models.WeatherReport, 'update')
    @mock.patch.object(models.AudioReport, 'update')
    @mock.patch.object(models.Report, 'update')
    def test_report_action_update(
            self, mock_update, mock_audio_update, mock_weather_update):
        '''Does _report(), call update() with the report provided when the
        action passed is models.Report.update, then recursively call the
        update() of nested reports within the report provided? 
        '''
        # TODO (jsa): mock function name discovery
        pipeline._report(self.report, 'report', models.Report.update)
        mock_update.assert_called_once_with(
            **{k: v for k, v in self.report if not isinstance(v, dict)})
        mock_audio_update.assert_called_once_with(**{self.report['audio']})
        mock_weather_update.assert_called_once_with(
            **{self.report['weather']})

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
    @mock.patch.object(pipeline, '_report')
    def test_update_snapshot(
            self, mock_update_report, mock_update_response, mock_get_accessor):
        '''Does update_snapshot() call _report() with the report included in
        the snapshot with the action models.Report.update, then call 
        get_response_accessor() with the response and report included in the
        snapshot, and finally call _response with the response included in the
        snapshot with the action numeric_accessor.update?
        '''
        mock_get_accessor.return_value = (
            pipeline.codec.numeric_accessor,
            {'question_id': 1, 'report_id': self.report['uniqueIdentifier']})
        pipeline.update_snapshot(self.snapshot)
        mock_update_report.assert_called_once_with(
            self.report, 'report', models.Report.update)
        mock_get_accessor.assert_called_once_with(
            self.response[0], self.report)
        mock_update_response.assert_called_once_with(
            self.response[0], pipeline.codec.numeric_accessor.update,
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
        pipeline._response(self.response,
                           pipeline.codec.numeric_accessor.delete)
        delete.assert_called_once_with(self.response)

    @mock.patch.object(models.WeatherReport, 'delete')
    @mock.patch.object(models.AudioReport, 'delete')
    @mock.patch.object(models.Report, 'delete')
    def test_report_action_delete(
            self, mock_delete, mock_audio_delete, mock_weather_delete):
        '''Does _report(), call delete() with the report provided when the
        action passed is models.Report.delete, then recursively call the
        delete() of nested reports within the report provided? 
        '''
        # TODO (jsa): mock function name discovery
        pipeline._report(self.report, 'report', models.Report.delete)
        mock_delete.assert_called_once_with(
            **{k: v for k, v in self.report if not isinstance(v, dict)})
        mock_audio_delete.assert_called_once_with(**{self.report['audio']})
        mock_weather_delete.assert_called_once_with(
            **{self.report['weather']})

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
