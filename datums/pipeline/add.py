from dateutil.parser import parse
import uuid
import json

from datums import models


# TODO: move these bad boys elsewhere...
token_accessor = models.base.ResponseClassLegacyAccessor(
    models.TokenResponse, 'tokens_response', 
    (lambda x: [i['text'] for i in x.get('tokens', [])]))

multi_accessor = models.base.ResponseClassLegacyAccessor(
    models.MultiResponse, 'multi_response',
    (lambda x: x.get('answeredOptions')))

boolean_accessor = models.base.ResponseClassLegacyAccessor(
    models.BooleanResponse, 'boolean_response',
    (lambda x: bool(x.get('answeredOptions'))))

location_accessor = models.base.LocationResponseClassLegacyAccessor(
    models.LocationResponse, 'location_response',  
    (lambda x: x['locationResponse'].get(
        'text') if x.get('locationResponse') else None),
    'venue_id', (lambda x: x['locationResponse'].get(
        'foursquareVenueId') if x.get('locationResponse') else None))

people_accessor = models.base.ResponseClassLegacyAccessor(
    models.PeopleResponse, 'people_response',
    (lambda x: [i['text'] for i in x.get('tokens', [])]))

numeric_accessor = models.base.ResponseClassLegacyAccessor(
    models.NumericResponse, 'numeric_response',
    (lambda x: x.get('numericResponse')))

note_accessor = models.base.ResponseClassLegacyAccessor(
    models.NoteResponse, 'numeric_response', (lambda x: x.get('noteResponse')))


def add_question(question):
    question_dict = {'type': question['questionType'],
                     'prompt': question['prompt']}
    models.Question.get_or_create(**question_dict)


def add_snapshot(snapshot):
    snapshot_dict = {
        'id': uuid.UUID(snapshot['uniqueIdentifier']),
        'created_at': parse(snapshot.get('date')),
        'report_impetus': snapshot.get('reportImpetus'),
        'battery': snapshot.get('battery'), 'steps': snapshot.get('steps'),
        'section_identifier': snapshot.get('sectionIdentifier'),
        'background': snapshot.get('background'),
        'connection': snapshot.get('connection'), 
        'draft': bool(snapshot.get('draft'))}
    models.Snapshot.get_or_create(**snapshot_dict)


def add_audio_snapshot(snapshot):
    audio_snapshot = snapshot['audio']
    audio_snapshot_dict = {
        'id': uuid.UUID(audio_snapshot['uniqueIdentifier']),
        'snapshot_id': uuid.UUID(snapshot['uniqueIdentifier']),
        'average': audio_snapshot.get('avg'),
        'peak': audio_snapshot.get('peak')}
    models.AudioSnapshot.get_or_create(**audio_snapshot_dict)


def add_location_snapshot(snapshot):
    location_snapshot = snapshot['location']
    location_snapshot_dict = {
        'id': uuid.UUID(location_snapshot['uniqueIdentifier']),
        'snapshot_id': uuid.UUID(snapshot['uniqueIdentifier']),
        'created_at': parse(str(location_snapshot.get('timestamp'))),
        'latitude': location_snapshot.get('latitude'),
        'longitude': location_snapshot.get('longitude'),
        'altitude': location_snapshot.get('altitude'),
        'speed': location_snapshot.get('speed'),
        'course': location_snapshot.get('course'),
        'vertical_accuracy': location_snapshot.get('verticalAccuracy'),
        'horizontal_accuracy': location_snapshot.get('horizontalAccuracy')}
    models.LocationSnapshot.get_or_create(**location_snapshot_dict)


def add_placemark_snapshot(snapshot):
    placemark_snapshot = snapshot['location']['placemark']
    placemark_snapshot_dict = {
        'id': uuid.UUID(placemark_snapshot.get('uniqueIdentifier')),
        'location_snapshot_id': uuid.UUID(
            snapshot['location']['uniqueIdentifier']),
        'street_number': placemark_snapshot.get('subThoroughfare'),
        'street_name': placemark_snapshot.get('thoroughfare'),
        'address': placemark_snapshot.get('name'),
        'neighborhood': placemark_snapshot.get('subLocality'),
        'city': placemark_snapshot.get('locality'),
        'county': placemark_snapshot.get('subAdministrativeArea'),
        'state': placemark_snapshot.get('administrativeArea'),
        'country': placemark_snapshot.get('country'),
        'postal_code': placemark_snapshot.get('postalCode'),
        'region': placemark_snapshot.get('region')}
    models.PlacemarkSnapshot.get_or_create(**placemark_snapshot_dict)


def add_weather_snapshot(snapshot):
    weather_snapshot = snapshot['weather']
    weather_snapshot_dict = {
        'id': weather_snapshot['uniqueIdentifier'],
        'snapshot_id': snapshot['uniqueIdentifier'],
        'station_id': weather_snapshot.get('stationID'),
        'latitude': weather_snapshot.get('latitude'),
        'longitude': weather_snapshot.get('longitude'),
        'weather': weather_snapshot.get('weather'), 
        'temperature_fahrenheit': weather_snapshot.get('tempF'),
        'temperature_celsius': weather_snapshot.get('tempC'),
        'feels_like_fahrenheit': weather_snapshot.get('feelslikeF'),
        'feels_like_celsius': weather_snapshot.get('feelslikeC'),
        'wind_direction': weather_snapshot.get('windDirection'),
        'wind_degrees': weather_snapshot.get('windDegrees'),
        'wind_mph': weather_snapshot.get('windMPH'),
        'wind_kph': weather_snapshot.get('windKPH'),
        'wind_gust_mph': weather_snapshot.get('windGustMPH'),
        'wind_gust_kph': weather_snapshot.get('windGustKPH'),
        'relative_humidity': weather_snapshot.get('relativeHumidity'),
        'precipitation_in': weather_snapshot.get('precipTodayIn'),
        'precipitation_mm': weather_snapshot.get('precipTodayMetric'),
        'dewpoint_celsius': weather_snapshot.get('dewpointC'),
        'visibility_mi': weather_snapshot.get('visibilityMi'),
        'visibility_km': weather_snapshot.get('visibilityKM'),
        'uv': weather_snapshot.get('uv')}
    models.WeatherSnapshot.get_or_create(**weather_snapshot_dict)


def add_response(response, snapshot):
    # Determine the question ID and response type based on the prompt
    question_id, response_type = models.session.query(
        models.Question.id, models.Question.type).filter(
            models.Question.prompt == response['questionPrompt']).first()
    print 'Snapshot ID: %s -----> Question ID: %s' % (
        snapshot['uniqueIdentifier'], question_id)

    ids = {'question_id': question_id,  # set the question ID
           'snapshot_id': snapshot['uniqueIdentifier']}  # set the snapshot ID

    # Dictionary mapping response type to response class, column, and accessor
    # mapper
    response_mapper = {0: token_accessor, 1: multi_accessor,
                       2: boolean_accessor, 3: location_accessor,
                       4: people_accessor, 5: numeric_accessor,
                       6: note_accessor}

    response_mapper[response_type].get_or_create_from_legacy_response(
        response, **ids)


def add_report(snapshot):
    # Add snapshots
    add_snapshot(snapshot)
    add_audio_snapshot(snapshot)
    add_location_snapshot(snapshot)
    add_placemark_snapshot(snapshot)
    add_weather_snapshot(snapshot)
    # Add responses
    for response in snapshot['responses']:
        add_response(response, snapshot)


def bulk_add_reports(files):
    if not isinstance(files, list):
        files = [files]
    # Add all reports for the files in files
    for file in files:
        with open(file, 'r') as f:
            report = json.load(f)
        # Add questions
        for question in report['questions']:
            add_question(question)
        for snapshot in report['snapshots']:
            add_report(snapshot)
