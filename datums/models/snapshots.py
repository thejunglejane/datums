from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, Numeric, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import UUIDType

from base import GhostBase

__all__ = ['Snapshot', 'AudioSnapshot', 'LocationSnapshot',
           'PlacemarkSnapshot', 'WeatherSnapshot']


class Snapshot(GhostBase):

    __tablename__ = 'snapshots'

    id = Column(UUIDType, primary_key=True)  # uniqueIdentifier
    created_at = Column(DateTime)  # date
    report_impetus = Column(Integer)  # reportImpetus
    battery = Column(Numeric)  # battery
    steps = Column(Integer)  # steps
    section_identifier = Column(String)  # sectionIdentifier
    background = Column(Numeric)  # background
    connection = Column(Numeric)  # connection
    draft = Column(Boolean)  # draft

    responses = relationship(
        'Response', backref=backref('snapshot', order_by=id))
    audio_snapshot = relationship(
        'AudioSnapshot', backref=backref('snapshot'))
    location_snapshot = relationship(
        'LocationSnapshot', backref=backref('snapshot'))
    weather_snapshot = relationship(
        'WeatherSnapshot', backref=backref('snapshot'))

    def __str__(self):
        attrs = ['id', 'created_at', 'report_impetus', 'battery', 'steps',
            'section_identifier', 'background', 'connection', 'draft']
        super(Snapshot, self).__str__(attrs)

class AudioSnapshot(GhostBase):

    __tablename__ = 'audio_snapshots'

    id = Column(UUIDType, primary_key=True)  # uniqueIdentifier
    snapshot_id = Column(UUIDType, ForeignKey(
        'snapshots.id'))  # uniqueIdentifier
    average = Column(Numeric)  # avg
    peak = Column(Numeric)  # peak

    def __str__(self):
        attrs = ['id', 'snapshot_id', 'average', 'peak']
        super(AudioSnapshot, self).__str__(attrs)


class LocationSnapshot(GhostBase):

    __tablename__ = 'location_snapshots'

    id = Column(UUIDType, primary_key=True)  # uniqueIdentifier
    snapshot_id = Column(UUIDType, ForeignKey(
        'snapshots.id'))  # uniqueIdentifier
    created_at = Column(DateTime)  # timestamp
    latitude = Column(Numeric)  # latitude
    longitude = Column(Numeric)  # longitude
    altitude = Column(Numeric)  # altitude
    speed = Column(Numeric)  # speed
    course = Column(Numeric)  # course
    vertical_accuracy = Column(Numeric)  # verticalAccuracy
    horizontal_accuracy = Column(Numeric)  # horizontalAccuracy

    placemark = relationship(
        'PlacemarkSnapshot', backref=backref('location_snapshots', order_by=id))

    def __str__(self):
        attrs = ['id', 'snapshot_id', 'created_at', 'latitude',
            'longitudue', 'altitude', 'speed', 'course',
            'vertical_accuracy', 'horizontal_accuracy']
        super(LocationSnapshot, self).__str__(attrs)


class PlacemarkSnapshot(GhostBase):

    __tablename__ = 'placemark_snapshots'

    id = Column(UUIDType, primary_key=True)   # uniqueIdentifier
    location_snapshot_id = Column(UUIDType, ForeignKey(
        'location_snapshots.id'))  # uniqueIdentifier
    street_number = Column(String)  # subThoroughfare
    street_name = Column(String)  # thoroughfare
    address = Column(String)  # name
    neighborhood = Column(String)  # subLocality
    city = Column(String)  # locality
    county = Column(String)  # subAdministrativeArea
    state = Column(String)  # administrativeArea
    country = Column(String)  # country
    postal_code = Column(String)  # postalCode
    region = Column(String)  # region

    def __str__(self):
        attrs = ['id', 'location_snapshot_id', 'street_number', 
            'street_name', 'address', 'neighborhood', 'city', 'county', 
            'state', 'country', 'postal_code', 'region']
        super(PlacemarkSnapshot, self).__str__(attrs)


class WeatherSnapshot(GhostBase):

    __tablename__ = 'weather_snapshots'

    id = Column(UUIDType, primary_key=True)  # uniqueIdentifier
    snapshot_id = Column(UUIDType, ForeignKey(
        'snapshots.id'))  # uniqueIdentifier
    station_id = Column(String)  # stationID
    latitude = Column(Numeric)  # latitude
    longitude = Column(Numeric)  # longitude
    weather = Column(String)  # weather
    temperature_fahrenheit = Column(Numeric)  # tempF
    temperature_celsius = Column(Numeric)  # tempC
    feels_like_fahrenheit = Column(Numeric)  # feelslikeF
    feels_like_celsius = Column(Numeric)  # feelslikeC
    wind_direction = Column(String)  # windDirection
    wind_degrees = Column(Integer)  # windDegrees
    wind_mph = Column(Numeric)  # windMPH
    wind_kph = Column(Numeric)  # windKPH
    wind_gust_mph = Column(Numeric)  # windGustMPH
    wind_gust_kph = Column(Numeric)  # windGustKPH
    relative_humidity = Column(String)  # relativeHumidity
    precipitation_in = Column(Numeric)  # precipTodayIn
    precipitation_mm = Column(Numeric)  # precipTodayMetric
    dewpoint_celsius = Column(Numeric)  # dewpointC
    visibility_mi = Column(Numeric)  # visibilityMi
    visibility_km = Column(Numeric)  # visibilityKM
    uv = Column(Numeric)  # uv

    def __str__(self):
        attrs = ['id', 'snapshot_id', 'station_id', 'latitude', 
            'longitude', 'weather', 'temperature_fahrenheit',
            'temperature_celsius', 'feels_like_fahrenheit',
            'feels_like_celsius', 'wind_direction', 'wind_degrees',
            'wind_mph', 'wind_kph', 'wind_gust_mph', 'wind_gust_kph',
            'relative_humidity', 'precipitation_in', 'precipitation_mm',
            'dewpoint_celsius', 'visibility_mi', 'visibility_km', 'uv']
        super(WeatherSnapshot, self).__str__(attrs)
