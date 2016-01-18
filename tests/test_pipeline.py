# -*- coding: utf-8 -*-

import mock
import random
import unittest
import uuid
from dateutil.parser import parse
from datums import models
from datums.pipeline import add, codec, delete, mappers, update
from sqlalchemy.orm import query


class TestPipelineAdd(unittest.TestCase):

    _response_classes = models.Response.__subclasses__()

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
            }
        }
        self.response = {'questionPrompt': 'How anxious are you?',
                         'uniqueIdentifier': 'B47C8530-BDFF-441A-AD82-36CD01B2DC6C',
                         'numericResponse': '1'}
        self.question = {'questionType': 'numeric',
                         'prompt': 'How anxious are you?'}

    def tearDown(self):
        del self.snapshot
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

    # @mock.patch.object(add, 'add_snaphot')
    # def test_add_report(
    #         self, mock_snapshot, mock_audio, mock_location,
    #         mock_placemark, mock_weather, mock_response):
    #     pass

    @mock.patch.object(models.base.ResponseClassLegacyAccessor,
                       'get_or_create_from_legacy_response')
    @mock.patch.object(codec, 'get_response_accessor')
    def test_add_response(self, mock_get_accessor, mock_get_response):
        '''Does add_response() call get_reponse_accessor() and
        get_or_create_from_legacy_response()?
        '''
        _accessor = models.base.ResponseClassLegacyAccessor(
            response_class=random.choice(self._response_classes),
            column='foo_response', accessor=(lambda x: x.get('foo')))
        _ids = {'foo': 'bar'}
        mock_get_accessor.return_value = _accessor, _ids
        add.add_response(self.response, self.snapshot)
        mock_get_accessor.assert_called_once_with(self.response, self.snapshot)
        mock_get_response.assert_called_once_with(self.response, **_ids)

    @mock.patch.object(models.AudioSnapshot, 'get_or_create')
    def test_add_snapshot(self, mock_get_create):
        '''Does add_snapshot() call get_or_create() with the snapshot info in
        the snapshot passed, and recurse nested snapshots within the snapshot? 
        '''
        self.snapshot['audio']['snapshotUniqueIdentifier'] = uuid.UUID(
            self.snapshot['uniqueIdentifier'])
        add.add_snapshot(
            self.snapshot['audio'], 'audio', mappers._snapshot_key_mapper['audio'])
        mock_get_create.assert_called_once_with(
            **{'average': 5, 'id': uuid.UUID(
                self.snapshot['audio']['uniqueIdentifier']), 'peak': 10,
                    'snapshot_id': uuid.UUID(self.snapshot['uniqueIdentifier'])})


# class TestPipelineUpdate(unittest.TestCase):

#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass


# class TestPipelineDelete(unittest.TestCase):

#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass
