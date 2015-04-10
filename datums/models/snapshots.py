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

    def __repr__(self):
        return '''<Snapshot(created_at='%s', report_impetus='%s', battery='%s',
            steps='%s', section_identifier='%s', background='%s',
            connection='%s', draft='%s')>''' % (
                self.created_at, self.report_impetus, self.battery, self.steps,
                self.section_identifier, self.background, self.connection,
                self.draft)


class AudioSnapshot(GhostBase):

    __tablename__ = 'audio_snapshots'

    id = Column(UUIDType, primary_key=True)  # uniqueIdentifier
    snapshot_id = Column(UUIDType, ForeignKey('snapshots.id'))  # uniqueIdentifier
    average = Column(Numeric)  # avg
    peak = Column(Numeric)  # peak

    def __repr__(self):
        return "<AudioSnapshot(average='%s', peak='%s')>" % (self.average,
                                                             self.peak)


class LocationSnapshot(GhostBase):

    __tablename__ = 'location_snapshots'

    id = Column(UUIDType, primary_key=True)  # uniqueIdentifier
    snapshot_id = Column(UUIDType, ForeignKey('snapshots.id'))  # uniqueIdentifier
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

    def __repr__(self):
        return '''<LocationSnapshot(created_at='%s', latitude='%s',
            longitude='%s', altitude='%s', speed='%s', course='%s',
            vertical_accuracy='%s', horizontal_accuracy='%s')>''' % (
                self.created_at, self.latitude, self.longitude, self.altitude,
                self.speed, self.course, self.vertical_accuracy,
                self.horizontal_accuracy)


class PlacemarkSnapshot(GhostBase):

    __tablename__ = 'placemark_snapshots'

    id = Column(UUIDType, primary_key=True)   # uniqueIdentifier
    location_snapshot_id = Column(UUIDType, ForeignKey('location_snapshots.id'))  # uniqueIdentifier
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

    def __repr__(self):
        return '''<PlacemarkSnapshot(street_number='%s', 'street_name'='%s',
            address='%s', neighborhood='%s', city='%s', county='%s', state='%s',
            country='%s', postal_code='%s', region='%s')>''' % (
                self.street_number, self.street_name, self.address,
                self.neighborhood, self.city, self.county, self.state,
                self.country, self.postal_code, self.region)


class WeatherSnapshot(GhostBase):

    __tablename__ = 'weather_snapshots'

    id = Column(UUIDType, primary_key=True)  # uniqueIdentifier
    snapshot_id = Column(UUIDType, ForeignKey('snapshots.id'))  # uniqueIdentifier
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

    def __repr__(self):
        return '''<WeatherSnapshot(station_id='%s', latitude='%s',
            longitude='%s', weather='%s', temperature_fahrenheit='%s',
            temperature_celsius='%s', feels_like_fahrenheit='%s',
            feels_like_celsius='%s', wind_direction='%s', wind_degrees='%s',
            wind_mph='%s', wind_kph='%s', wind_gust_mph='%s',
            wind_gust_kph='%s', relative_humidity='%s', precipitation_in='%s',
            precipitation_mm='%s', dewpoint_celsius='%s', visibility_mi='%s',
            visibility_km='%s', uv='%s')>''' % (
                self.station_id, self.latitude, self.longitude, self.weather,
                self.temperature_fahrenheit, self.temperature_celsius,
                self.feels_like_fahrenheit, self.feels_like_celsius,
                self.wind_direction, self.wind_degrees, self.wind_mph,
                self.wind_kph, self.wind_gust_mph, self.wind_gust_kph,
                self.relative_humidity, self.precipitation_in,
                self.precipitation_mm, self.dewpoint_celsius,
                self.visibility_mi, self.visibility_km, self.uv)

