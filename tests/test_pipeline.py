# -*- coding: utf-8 -*-

from dateutil.parser import parse
from datums import models
from datums import pipeline
from sqlalchemy.orm import query
import mock
import random
import unittest
import uuid


class TestPipelineAdd(unittest.TestCase):

    _response_classes = models.Response.__subclasses__()

    def setUp(self):
        self.snapshot = {
            'uniqueIdentifier': 'f2b8805c-b107-462d-b6ff-d67532ef797b',
            'date': '2015-03-22T09:10:35-0400', 'reportImpetus': 4,
            'battery': 0.80, 'steps': 100, 'sectionIdentifier': '1-2016-1-14',
            'background': 0, 'connection': 0, 'draft': 0, 'audio': {
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
        self.response = {}
        self.question = {'questionType': 'numeric',
                         'prompt': 'How happy are you?'}

    def tearDown(self):
        del self.snapshot
        del self.response
        del self.question

    # @mock.patch.object(add, 'add_response')
    # @mock.patch.object(add, 'add_weather_snaphot')
    # @mock.patch.object(add, 'add_placemark_snaphot')
    # @mock.patch.object(add, 'add_location_snaphot')
    # @mock.patch.object(add, 'add_audio_snaphot')
    # @mock.patch.object(add, 'add_snaphot')
    # def test_add_report(
    #         self, mock_snapshot, mock_audio, mock_location,
    #         mock_placemark, mock_weather, mock_response):
    #     pass

    @mock.patch.object(models.base.ResponseClassLegacyAccessor,
                       'get_or_create_from_legacy_response')
    @mock.patch.object(pipeline.codec, 'get_response_accessor')
    def test_add_response(self, mock_get_accessor, mock_get_response):
        '''Does add_response() call get_reponse_accessor() and
        get_or_create_from_legacy_response()?
        '''
        _accessor = models.base.ResponseClassLegacyAccessor(
            response_class=random.choice(self._response_classes),
            column='foo_response', accessor=(lambda x: x.get('foo')))
        _ids = {'foo': 'bar'}
        mock_get_accessor.return_value = _accessor, _ids
        pipeline.add.add_response(self.response, self.snapshot)
        mock_get_accessor.assert_called_once_with(self.response, self.snapshot)
        mock_get_response.assert_called_once_with(self.response, **_ids)

    @mock.patch.object(models.Question, 'get_or_create')
    def test_add_question(self, mock_get_create):
        '''Does add_question() call get_or_create() with the question type and
        prompt specified in the question passed? 
        '''
        pipeline.add.add_question(self.question)
        mock_get_create.assert_called_once_with(
            **{'type': self.question['questionType'],
               'prompt': self.question['prompt']})

    @mock.patch.object(models.Snapshot, 'get_or_create')
    def test_add_snapshot(self, mock_get_create):
        '''Does add_snapshot() call get_or_create() with the snapshot info in
        the snapshot passed? 
        '''
        pipeline.add.add_snapshot(self.snapshot)
        mock_get_create.assert_called_once_with(
            **{'id': uuid.UUID(self.snapshot['uniqueIdentifier']),
               'created_at': parse(self.snapshot['date']),
               'report_impetus': self.snapshot['reportImpetus'],
               'battery': self.snapshot['battery'],
               'steps': self.snapshot['steps'],
               'section_identifier': self.snapshot['sectionIdentifier'],
               'background': self.snapshot['background'],
               'connection': self.snapshot['connection'],
               'draft': bool(self.snapshot['draft'])})

    @mock.patch.object(models.AudioSnapshot, 'get_or_create')
    def test_add_audio_snapshot(self, mock_get_create):
        '''Does add_audio_snapshot() call get_or_create() with the audio
        snapshot info in the audio snapshot passed? 
        '''
        pipeline.add.add_audio_snapshot(self.snapshot)
        mock_get_create.assert_called_once_with(
            **{'id': uuid.UUID(self.snapshot['audio']['uniqueIdentifier']),
               'snapshot_id': uuid.UUID(self.snapshot['uniqueIdentifier']),
               'average': self.snapshot['audio']['avg'],
               'peak': self.snapshot['audio']['peak']})

    # @mock.patch.object(pipeline.add, 'add_placemark_snaphot')
    # @mock.patch.object(models.LocationSnapshot, 'get_or_create')
    # def test_add_location_snapshot(self, mock_get_create):
    #     '''Does add_location_snaphot call get_or_create() with the location
    #     snapshot info in the snapshot passed?
    #     '''
    #     pass

    # @mock.patch.object(pipeline.add, 'add_placemark_snaphot')
    # @mock.patch.object(models.LocationSnapshot, 'get_or_create')
    # def test_add_location_snapshot_no_snapshot(self, mock_get_create):
    #     '''Does add_location_snaphot not call get_or_create() if there is no
    #     location snapshot included in the snapshot?
    #     '''
    #     pass

    @mock.patch.object(models.PlacemarkSnapshot, 'get_or_create')
    def test_add_placemark_snapshot(self, mock_get_create):
        '''Does add_placemark_snaphot call get_or_create() with the placemark
        snapshot info in the location snapshot passed?
        '''
        # pipeline.add.add_placemark_snaphot(self.snapshot)
        pass

    @mock.patch.object(models.PlacemarkSnapshot, 'get_or_create')
    def test_add_placemark_snapshot_no_snapshot(self, mock_get_create):
        '''Does add_placemark_snaphot not call get_or_create() if there is no
        placemark snapshot included in the location snapshot?
        '''
        # self.snapshot['location'].pop('placemark', None)
        pass

    @mock.patch.object(models.WeatherSnapshot, 'get_or_create')
    def test_add_weather_snapshot(self, mock_get_create):
        '''Does add_weather_snapshot() call get_or_create() with the weather
        snapshot info in the weather snapshot passed? 
        '''
        pipeline.add.add_weather_snapshot(self.snapshot)
        mock_get_create.assert_called_once_with(
            **{'id': uuid.UUID(self.snapshot['weather']['uniqueIdentifier']),
               'snapshot_id': uuid.UUID(self.snapshot['uniqueIdentifier']),
               'station_id': self.snapshot['weather']['stationID'],
               'latitude': self.snapshot['weather']['latitude'],
               'longitude': self.snapshot['weather']['longitude'],
               'weather': self.snapshot['weather']['weather'],
               'temperature_fahrenheit': self.snapshot['weather']['tempF'],
               'temperature_celsius': self.snapshot['weather']['tempC'],
               'feels_like_fahrenheit': self.snapshot['weather']['feelslikeF'],
               'feels_like_celsius': self.snapshot['weather']['feelslikeC'],
               'wind_direction': self.snapshot['weather']['windDirection'],
               'wind_degrees': self.snapshot['weather']['windDegrees'],
               'wind_mph': self.snapshot['weather']['windMPH'],
               'wind_kph': self.snapshot['weather']['windKPH'],
               'wind_gust_mph': self.snapshot['weather']['windGustMPH'],
               'wind_gust_kph': self.snapshot['weather']['windGustKPH'],
               'relative_humidity': self.snapshot[
                    'weather']['relativeHumidity'],
               'precipitation_in': self.snapshot['weather']['precipTodayIn'],
               'precipitation_mm': self.snapshot[
                    'weather']['precipTodayMetric'],
               'dewpoint_celsius': self.snapshot['weather']['dewpointC'],
               'visibility_mi': self.snapshot['weather']['visibilityMi'],
               'visibility_km': self.snapshot['weather']['visibilityKM'],
               'uv': self.snapshot['weather']['uv']
               })

    @mock.patch.object(models.WeatherSnapshot, 'get_or_create')
    def test_add_weather_snapshot_no_snapshot(self, mock_get_create):
        '''Does add_weather_snapshot() not call get_or_create() if there is no
        weather info in the snapshot passed? 
        '''
        self.snapshot.pop('weather', None)
        pipeline.add.add_weather_snapshot(self.snapshot)
        mock_get_create.assert_not_called()


class TestPipelineUpdate(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestPipelineDelete(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
