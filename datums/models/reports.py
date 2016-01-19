# -*- coding: utf-8 -*-

from base import GhostBase
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, Numeric, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import UUIDType


__all__ = ['Report', 'AltitudeReport', 'AudioReport',
           'LocationReport', 'PlacemarkReport', 'WeatherReport']


class Report(GhostBase):

    __tablename__ = 'reports'

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
        'Response', backref=backref('Report', order_by=id, cascade='delete'))
    altitude_report = relationship(
        'AltitudeReport', backref=backref('Report'), cascade='delete')
    audio_report = relationship(
        'AudioReport', backref=backref('Report'), cascade='delete')
    location_report = relationship(
        'LocationReport', backref=backref('Report'), cascade='delete')
    weather_report = relationship(
        'WeatherReport', backref=backref('Report'), cascade='delete')

    def __str__(self):
        attrs = ['id', 'created_at', 'report_impetus', 'battery', 'steps',
            'section_identifier', 'background', 'connection', 'draft']
        super(report, self).__str__(attrs)

class AltitudeReport(GhostBase):

    __tablename__ = 'altitude_reports'

    id = Column(UUIDType, primary_key=True)
    floors_ascended = Column(Numeric)
    floors_descended = Column(Numeric)
    gps_altitude_from_location = Column(Numeric)
    gps_altitude_raw = Column(Numeric)
    pressure = Column(Numeric)
    pressure_adjusted = Column(Numeric)
    report_id = Column(UUIDType, ForeignKey('reports.id'), nullable=False)

    def __str__(self):
        attrs = ['id', 'report_id', 'average', 'peak']
        super(AltitudeReport, self).__str__(attrs)
        

class AudioReport(GhostBase):

    __tablename__ = 'audio_reports'

    id = Column(UUIDType, primary_key=True)
    average = Column(Numeric)
    peak = Column(Numeric)
    report_id = Column(UUIDType, ForeignKey('reports.id'), nullable=False)

    def __str__(self):
        attrs = ['id', 'report_id', 'average', 'peak']
        super(AudioReport, self).__str__(attrs)


class LocationReport(GhostBase):

    __tablename__ = 'location_reports'

    id = Column(UUIDType, primary_key=True)
    altitude = Column(Numeric)
    course = Column(Numeric)
    created_at = Column(DateTime)
    horizontal_accuracy = Column(Numeric)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    report_id = Column(UUIDType, ForeignKey('reports.id'), nullable=False)
    speed = Column(Numeric)
    vertical_accuracy = Column(Numeric)

    placemark = relationship(
        'PlacemarkReport', backref=backref('location_reports', order_by=id))

    def __str__(self):
        attrs = ['id', 'report_id', 'created_at', 'latitude',
            'longitudue', 'altitude', 'speed', 'course',
            'vertical_accuracy', 'horizontal_accuracy']
        super(LocationReport, self).__str__(attrs)


class PlacemarkReport(GhostBase):

    __tablename__ = 'placemark_reports'

    id = Column(UUIDType, primary_key=True)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    county = Column(String)
    inland_water = Column(String)
    location_report_id = Column(
        UUIDType, ForeignKey('location_reports.id'), nullable=False)
    neighborhood = Column(String)
    postal_code = Column(String)
    region = Column(String)
    state = Column(String)
    street_name = Column(String)
    street_number = Column(String)

    def __str__(self):
        attrs = ['id', 'location_report_id', 'street_number', 
            'street_name', 'address', 'neighborhood', 'city', 'county', 
            'state', 'country', 'postal_code', 'region']
        super(PlacemarkReport, self).__str__(attrs)


class WeatherReport(GhostBase):

    __tablename__ = 'weather_reports'

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
    report_id = Column(UUIDType, ForeignKey('reports.id'), nullable=False)
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
        attrs = ['id', 'report_id', 'station_id', 'latitude', 
            'longitude', 'weather', 'temperature_fahrenheit',
            'temperature_celsius', 'feels_like_fahrenheit',
            'feels_like_celsius', 'wind_direction', 'wind_degrees',
            'wind_mph', 'wind_kph', 'wind_gust_mph', 'wind_gust_kph',
            'relative_humidity', 'precipitation_in', 'precipitation_mm',
            'dewpoint_celsius', 'visibility_mi', 'visibility_km', 'uv']
        super(WeatherReport, self).__str__(attrs)
