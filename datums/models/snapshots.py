from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, Numeric, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import UUIDType

from base import GhostBase

__all__ = ['Snapshot', 'AltitudeSnapshot', 'AudioSnapshot',
           'LocationSnapshot', 'PlacemarkSnapshot', 'WeatherSnapshot']


class Snapshot(GhostBase):

    __tablename__ = 'snapshots'

    id = Column(UUIDType, primary_key=True)
    background = Column(Numeric)
    battery = Column(Numeric)
    connection = Column(Numeric)
    created_at = Column(DateTime)
    draft = Column(Boolean)
    report_impetus = Column(Integer)
    section_identifier = Column(String)
    steps = Column(Integer)

    responses = relationship(
        'Response', backref=backref('snapshot', order_by=id))
    altitude_snapshot = relationship(
        'AltitudeSnapshot', backref=backref('snapshot'))
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

class AltitudeSnapshot(GhostBase):

    __tablename__ = 'altitude_snapshots'

    id = Column(UUIDType, primary_key=True)
    floors_ascended = Column(Numeric)
    floors_descended = Column(Numeric)
    gps_altitude_from_location = Column(Numeric)
    gps_altitude_raw = Column(Numeric)
    pressure = Column(Numeric)
    pressure_adjusted = Column(Numeric)
    snapshot_id = Column(UUIDType, ForeignKey('snapshots.id'), nullable=False)

    def __str__(self):
        attrs = ['id', 'snapshot_id', 'average', 'peak']
        super(AudioSnapshot, self).__str__(attrs)
        

class AudioSnapshot(GhostBase):

    __tablename__ = 'audio_snapshots'

    id = Column(UUIDType, primary_key=True)
    average = Column(Numeric)
    peak = Column(Numeric)
    snapshot_id = Column(UUIDType, ForeignKey('snapshots.id'), nullable=False)

    def __str__(self):
        attrs = ['id', 'snapshot_id', 'average', 'peak']
        super(AudioSnapshot, self).__str__(attrs)


class LocationSnapshot(GhostBase):

    __tablename__ = 'location_snapshots'

    id = Column(UUIDType, primary_key=True)
    altitude = Column(Numeric)
    course = Column(Numeric)
    created_at = Column(DateTime)
    horizontal_accuracy = Column(Numeric)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    snapshot_id = Column(UUIDType, ForeignKey('snapshots.id'), nullable=False)
    speed = Column(Numeric)
    vertical_accuracy = Column(Numeric)

    placemark = relationship(
        'PlacemarkSnapshot', backref=backref('location_snapshots', order_by=id))

    def __str__(self):
        attrs = ['id', 'snapshot_id', 'created_at', 'latitude',
            'longitudue', 'altitude', 'speed', 'course',
            'vertical_accuracy', 'horizontal_accuracy']
        super(LocationSnapshot, self).__str__(attrs)


class PlacemarkSnapshot(GhostBase):

    __tablename__ = 'placemark_snapshots'

    id = Column(UUIDType, primary_key=True)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    county = Column(String)
    location_snapshot_id = Column(
        UUIDType, ForeignKey('location_snapshots.id'), nullable=False)
    neighborhood = Column(String)
    postal_code = Column(String)
    region = Column(String)
    state = Column(String)
    street_name = Column(String)
    street_number = Column(String)

    def __str__(self):
        attrs = ['id', 'location_snapshot_id', 'street_number', 
            'street_name', 'address', 'neighborhood', 'city', 'county', 
            'state', 'country', 'postal_code', 'region']
        super(PlacemarkSnapshot, self).__str__(attrs)


class WeatherSnapshot(GhostBase):

    __tablename__ = 'weather_snapshots'

    id = Column(UUIDType, primary_key=True)
    dewpoint_celsius = Column(Numeric)
    feels_like_celsius = Column(Numeric)
    feels_like_fahrenheit = Column(Numeric)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    precipitation_in = Column(Numeric)
    precipitation_mm = Column(Numeric)
    pressure_in = Column(Numeric)
    pressure_mb = Column(Numeric)
    relative_humidity = Column(String)
    snapshot_id = Column(UUIDType, ForeignKey('snapshots.id'), nullable=False)
    station_id = Column(String)
    temperature_celsius = Column(Numeric)
    temperature_fahrenheit = Column(Numeric)
    uv = Column(Numeric)
    visibility_km = Column(Numeric)
    visibility_mi = Column(Numeric)
    weather = Column(String)
    wind_degrees = Column(Integer)
    wind_direction = Column(String)
    wind_gust_kph = Column(Numeric)
    wind_gust_mph = Column(Numeric)
    wind_kph = Column(Numeric)
    wind_mph = Column(Numeric)

    def __str__(self):
        attrs = ['id', 'snapshot_id', 'station_id', 'latitude', 
            'longitude', 'weather', 'temperature_fahrenheit',
            'temperature_celsius', 'feels_like_fahrenheit',
            'feels_like_celsius', 'wind_direction', 'wind_degrees',
            'wind_mph', 'wind_kph', 'wind_gust_mph', 'wind_gust_kph',
            'relative_humidity', 'precipitation_in', 'precipitation_mm',
            'dewpoint_celsius', 'visibility_mi', 'visibility_km', 'uv']
        super(WeatherSnapshot, self).__str__(attrs)
