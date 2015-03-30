from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import sqlalchemy
import json
import time
import os


DATUMS_MODEL_PATH = os.environ['DATUMS_MODEL_PATH']
DATUMS_DB = os.environ['DATUMS_DB']  # postgres engine string
REPORTER_PATH = os.environ['REPORTER_PATH']

execfile(DATUMS_MODEL_PATH)  # Load table classes

# Gather all Reporter reports
report_files = [file for file in os.listdir(
    REPORTER_PATH) if file.endswith('.json')]

# Initialize database engine
engine = create_engine(DATUMS_DB, echo=False)
# Initialize session
Session = sessionmaker(bind=engine)


def add_snapshot(record):
    '''Given a snapshot record, create table instances for that record and 
    insert them into the Reporter database.'''
    # Define snapshot mappings
    snapshot_dict = {'id': str(record['uniqueIdentifier']), 'audio_snapshot_id': str(record['audio']['uniqueIdentifier']), 'location_snapshot_id': str(record['location']['uniqueIdentifier']), 'weather_snapshot_id': str(record['weather']['uniqueIdentifier']), 'created_at': datetime.fromtimestamp(
        time.mktime(time.strptime(str(record['date'][:-5]), '%Y-%m-%dT%H:%M:%S'))), 'report_impetus': record['reportImpetus'], 'battery': record['battery'], 'steps': record['steps'], 'floors_ascended': record['altitude']['floorsAscended'], 'floors_descended': record['altitude']['floorsDescended']}
    audio_snapshot_dict = {'id': str(record['audio']['uniqueIdentifier']), 'average': record[
        'audio']['avg'], 'peak': record['audio']['peak']}
    location_snapshot_dict = {'id': str(record['location']['uniqueIdentifier']), 'placemark_id': str(record['location']['placemark']['uniqueIdentifier']), 'created_at': datetime.fromtimestamp(time.mktime(time.strptime(str(record['location']['timestamp'][:-5]), '%Y-%m-%dT%H:%M:%S'))), 'latitude': record['location'][
        'latitude'], 'longitude': record['location']['longitude'], 'altitude': record['location']['altitude'], 'speed': record['location']['speed'], 'vertical_accuracy': record['location']['verticalAccuracy'], 'horizontal_accuracy': record['location']['horizontalAccuracy']}
    placemark_snapshot_dict = {'id': str(record['location']['placemark']['uniqueIdentifier']), 'street_address': None, 'neighborhood': str(record['location']['placemark']['subLocality']), 'city': str(record['location']['placemark'][
        'locality']), 'county': str(record['location']['placemark']['subAdministrativeArea']), 'state': str(record['location']['placemark']['administrativeArea']), 'country': str(record['location']['placemark']['country']), 'postal_code': record['location']['placemark']['postalCode']}
    weather_snapshot_dict = {'id': str(record['weather']['uniqueIdentifier']), 'station_id': str(record['weather']['stationID']), 'latitude': record['weather']['latitude'], 'longitude': record['weather']['longitude'], 'weather': str(record['weather']['weather']), 'temperature_fahrenheit': record['weather']['tempF'], 'temperature_celsius': record['weather']['tempC'], 'feels_like_fahrenheit': record['weather']['feelslikeF'], 'feels_like_celsius': record['weather']['feelslikeC'], 'wind_direction': record['weather']['windDirection'], 'wind_degrees': record['weather'][
        'windDegrees'], 'wind_mph': record['weather']['windMPH'], 'wind_kph': record['weather']['windKPH'], 'wind_gust_mph': record['weather']['windGustMPH'], 'wind_gust_kph': record['weather']['windGustKPH'], 'relative_humidity': record['weather']['relativeHumidity'], 'precipitation_in': record['weather']['precipTodayIn'], 'precipitation_mm': record['weather']['precipTodayMetric'], 'dewpoint_celsius': record['weather']['dewpointC'], 'visibility_mi': record['weather']['visibilityMi'], 'visibility_km': record['weather']['visibilityKM'], 'uv': record['weather']['uv']}

    # Handle common null problem with thoroughfare
    try:
        record['location']['placemark']['thoroughfare']
    except KeyError:
        pass
    else:
        placemark_snapshot_dict['street_address'] = str(
            record['location']['placemark']['thoroughfare'])

    # Open a session
    session = Session()

    new_snapshot = Snapshot(snapshot_dict)
    new_snapshot.audio_snapshot = AudioSnapshot(audio_snapshot_dict)
    new_snapshot.location_snapshot = LocationSnapshot(location_snapshot_dict)
    new_snapshot.location_snapshot.placemark = PlacemarkSnapshot(
        placemark_snapshot_dict)
    new_snapshot.weather_snapshot = WeatherSnapshot(weather_snapshot_dict)

    # Add the new snapshot to the database
    session.add(new_snapshot)
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError:  # skip records that already exist
        pass
    else:
        print snapshot_dict['created_at'], '--->', snapshot_dict['id']


# Add new report records to the database
for report_file in report_files:
    report = os.path.join(REPORTER_PATH, report_file)
    report = json.load(open(report))

    for snapshot in report['snapshots']:
        add_snapshot(snapshot)
