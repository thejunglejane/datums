from dateutil.parser import parse
import uuid
import json

from .. import models


def add_question(question):
    question_dict = {'type': question['questionType'],
                     'prompt': question['prompt']}
    models.Question.get_or_create(**question_dict)


def add_snapshot(snapshot):
    snapshot_dict = {'id': uuid.UUID(snapshot['uniqueIdentifier']),
                     'created_at': parse(snapshot['date']),
                     'report_impetus': snapshot['reportImpetus'],
                     'battery': snapshot['battery'],
                     'steps': snapshot['steps'],
                     'section_identifier': snapshot['sectionIdentifier'],
                     'background': snapshot['background'],
                     'connection': snapshot['connection'],
                     'draft': bool(snapshot['draft'])}
    models.Snapshot.get_or_create(**snapshot_dict)


def add_audio_snapshot(snapshot):
    audio_snapshot = snapshot['audio']
    audio_snapshot_dict = {'id': uuid.UUID(audio_snapshot['uniqueIdentifier']),
                           'snapshot_id': uuid.UUID(
                                snapshot['uniqueIdentifier']),
                           'average': audio_snapshot['avg'],
                           'peak': audio_snapshot['peak']}
    models.AudioSnapshot.get_or_create(**audio_snapshot_dict)


def add_location_snapshot(snapshot):
    location_snapshot = snapshot['location']
    location_snapshot_dict = {'id': uuid.UUID(
                                    location_snapshot['uniqueIdentifier']),
                              'snapshot_id': uuid.UUID(
                                    snapshot['uniqueIdentifier']),
                              'created_at': parse(
                                    str(location_snapshot['timestamp'])),
                              'latitude': location_snapshot['latitude'],
                              'longitude': location_snapshot['longitude'],
                              'altitude': location_snapshot['altitude'],
                              'speed': location_snapshot['speed'],
                              'course': location_snapshot['course'],
                              'vertical_accuracy': 
                                    location_snapshot['verticalAccuracy'],
                              'horizontal_accuracy': 
                                    location_snapshot['horizontalAccuracy']}
    models.LocationSnapshot.get_or_create(**location_snapshot_dict)


def add_placemark_snapshot(snapshot):
    placemark_snapshot = snapshot['location']['placemark']
    placemark_snapshot_dict = {'id': uuid.UUID(
                                    placemark_snapshot['uniqueIdentifier']),
                               'location_snapshot_id': uuid.UUID(
                                    snapshot['location']['uniqueIdentifier']),
                               'street_number': placemark_snapshot[
                                    'subThoroughfare'],
                               'street_name': None,
                               'address': placemark_snapshot['name'],
                               'neighborhood': placemark_snapshot[
                                    'subLocality'],
                               'city': placemark_snapshot['locality'],
                               'county': 
                                    placemark_snapshot['subAdministrativeArea'],
                               'state': 
                                    placemark_snapshot['administrativeArea'],
                               'country': placemark_snapshot['country'],
                               'postal_code': placemark_snapshot['postalCode'],
                               'region': placemark_snapshot['region']}
    
    if 'thoroughfare' in placemark_snapshot:
        placemark_snapshot_dict[
            'street_name'] = placemark_snapshot['thoroughfare']
    
    models.PlacemarkSnapshot.get_or_create(**placemark_snapshot_dict)


def add_weather_snapshot(snapshot):
    weather_snapshot = snapshot['weather']
    weather_snapshot_dict = {'id': weather_snapshot['uniqueIdentifier'],
                             'snapshot_id': snapshot['uniqueIdentifier'],
                             'station_id': weather_snapshot['stationID'],
                             'latitude': weather_snapshot['latitude'],
                             'longitude': weather_snapshot['longitude'],
                             'weather': weather_snapshot['weather'],
                             'temperature_fahrenheit': 
                                weather_snapshot['tempF'],
                             'temperature_celsius': weather_snapshot['tempC'],
                             'feels_like_fahrenheit':
                                weather_snapshot['feelslikeF'],
                             'feels_like_celsius':
                                weather_snapshot['feelslikeC'],
                             'wind_direction':
                                weather_snapshot['windDirection'],
                             'wind_degrees': weather_snapshot['windDegrees'],
                             'wind_mph': weather_snapshot['windMPH'],
                             'wind_kph': weather_snapshot['windKPH'],
                             'wind_gust_mph': weather_snapshot['windGustMPH'],
                             'wind_gust_kph': weather_snapshot['windGustKPH'],
                             'relative_humidity':
                                weather_snapshot['relativeHumidity'],
                             'precipitation_in':
                                weather_snapshot['precipTodayIn'],
                             'precipitation_mm':
                                weather_snapshot['precipTodayMetric'],
                             'dewpoint_celsius': weather_snapshot['dewpointC'],
                             'visibility_mi': weather_snapshot['visibilityMi'],
                             'visibility_km': weather_snapshot['visibilityKM'],
                             'uv': weather_snapshot['uv']}
    models.WeatherSnapshot.get_or_create(**weather_snapshot_dict)


def add_response(response, snapshot):
    question_info = {
        i.prompt: (i.id, i.type) for i in models.session.query(models.Question).all()}

    response_types = {0: models.TokenResponse, 1: models.MultiResponse,
                      2: models.BooleanResponse, 3: models.LocationResponse,
                      4: models.PeopleResponse, 5: models.NumericResponse,
                      6: models.NoteResponse}

    response_id, response_type = question_info[str(response['questionPrompt'])]
    response_cls = response_types[response_type]

    response_dict = {'snapshot_id': uuid.UUID(snapshot['uniqueIdentifier']),
                     'question_id': response_id}

    # TODO: handle empty response for any question
    if response_type == 0:
        response_dict['tokens_response'] = None
        if 'tokens' in response:
            response_dict['tokens_response'] = [
                i['text'] for i in response['tokens']]
    elif response_type == 1:
        response_dict['multi_response'] = [
            i for i in response['answeredOptions']].sort()
    elif response_type == 2:
        response_dict['boolean_response'] = bool(response['answeredOptions'])
    elif response_type == 3:
        location_response_record = response['locationResponse']
        response_dict['location_response'] = location_response_record['text']
        response_dict['venue_id'] = None
        if 'venue_id' in response:
            response_dict['venue_id'] = location_response['foursquareVenueId']
    elif response_type == 4:
        response_dict['tokens_response'] = None
        if 'tokens' in response:
            response_dict['tokens_response'] = [
                i['text'] for i in response['tokens']]
    elif response_type == 5:
        response_dict['numeric_response'] = response['numericResponse']
    elif response_type == 6:
        response_dict['note_response'] = response['noteResponse']
    
    response_cls.get_or_create(snapshot_id = response_dict['snapshot_id'],
                               question_id = response_dict['question_id'])
    # TODO: update record with additional information in response_dict


def add_report(report):
    # Add questions
    for question in report['questions']:
        add_question(question)
    # Add snapshots
    for snapshot in report['snapshots']:
        add_snapshot(snapshot)
        add_audio_snapshot(snapshot)
        add_location_snapshot(snapshot)
        add_weather_snapshot(snapshot)
        add_weather_snapshot(snapshot)
        # Add responses
        for response in snapshot['responses']:
            add_response(response, snapshot)


def update_report(report):
    pass


def delete_report(report):
    pass


def bulk_add_reports(files):
    if not isinstance(files, list):
        files = [files]
    # Add all reports for the files in files
    for file in files:
        with open(file, 'r') as f:
            report = json.load(f)
        add_report(report)
