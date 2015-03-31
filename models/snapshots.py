from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, Numeric, String, DateTime
from sqlalchemy.orm import relationship, backref

from datums.models import Base, metadata

__all__ = ['Snapshot', 'AudioSnapshot', 'LocationSnapshot',
           'PlacemarkSnapshot', 'WeatherSnapshot']


class Snapshot(Base):

    __tablename__ = 'snapshots'

    id = Column(String, primary_key=True)
    audio_snapshot_id = Column(String, ForeignKey('audio_snapshots.id'))
    location_snapshot_id = Column(String, ForeignKey('location_snapshots.id'))
    weather_snapshot_id = Column(String, ForeignKey('weather_snapshots.id'))
    created_at = Column(DateTime)
    report_impetus = Column(Integer)
    battery = Column(Numeric)
    steps = Column(Integer)
    floors_ascended = Column(Integer)
    floors_descended = Column(Integer)

    audio_snapshot = relationship(
        'AudioSnapshot', backref=backref('snapshots', order_by=id))
    location_snapshot = relationship(
        'LocationSnapshot', backref=backref('snapshots', order_by=id))
    weather_snapshot = relationship(
        'WeatherSnapshot', backref=backref('snapshots', order_by=id))

    def __repr__(self):
        return '''<Snapshot(created_at='%s', report_impetus='%s', battery='%s',
            steps='%s', floors_ascended='%s', floors_descended='%s')>''' % (
            self.created_at, self.report_impetus, self.battery, self.steps,
            self.floors_ascended, self.floors_descended)


class AudioSnapshot(Base):

    __tablename__ = 'audio_snapshots'

    id = Column(String, primary_key=True)
    average = Column(Numeric)
    peak = Column(Numeric)

    def __repr__(self):
        return "<AudioSnapshot(average='%s', peak='%s')>" % (self.average,
                                                             self.peak)


class LocationSnapshot(Base):

    __tablename__ = 'location_snapshots'

    id = Column(String, primary_key=True)
    placemark_id = Column(String, ForeignKey('placemark_snapshots.id'))
    created_at = Column(DateTime)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    altitude = Column(Numeric)
    speed = Column(Numeric)
    vertical_accuracy = Column(Numeric)
    horizontal_accuracy = Column(Numeric)

    placemark = relationship(
        'PlacemarkSnapshot', backref=backref('location_snapshots', order_by=id))

    def __repr__(self):
        return '''<LocationSnapshot(created_at='%s', latitude='%s',
            longitude='%s', altitude='%s', speed='%s', vertical_accuracy='%s',
            horizontal_accuracy='%s')>''' % (
            self.created_at, self.latitude, self.longitude, self.altitude,
            self.speed, self.vertical_accuracy, self.horizontal_accuracy)


class PlacemarkSnapshot(Base):

    __tablename__ = 'placemark_snapshots'

    id = Column(String, primary_key=True)
    street_address = Column(String)
    neighborhood = Column(String)
    city = Column(String)
    county = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)

    def __repr__(self):
        return '''<PlacemarkSnapshot(street_address='%s', neighborhood='%s', 
            city='%s', county='%s', state='%s', country='%s', 
            postal_code='%s')>''' % (self.street_address, self.neighborhood,
                                     self.city, self.county, self.state,
                                     self.country, self.postal_code)


class WeatherSnapshot(Base):

    __tablename__ = 'weather_snapshots'

    id = Column(String, primary_key=True)
    station_id = Column(String)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    weather = Column(String)
    temperature_fahrenheit = Column(Numeric)
    temperature_celsius = Column(Numeric)
    feels_like_fahrenheit = Column(Numeric)
    feels_like_celsius = Column(Numeric)
    wind_direction = Column(String)
    wind_degrees = Column(Integer)
    wind_mph = Column(Numeric)
    wind_kph = Column(Numeric)
    wind_gust_mph = Column(Numeric)
    wind_gust_kph = Column(Numeric)
    relative_humidity = Column(String)
    precipitation_in = Column(Numeric)
    precipitation_mm = Column(Numeric)
    dewpoint_celsius = Column(Numeric)
    visibility_mi = Column(Numeric)
    visibility_km = Column(Numeric)
    uv = Column(Numeric)

    def __repr__(self):
        return '''<WeatherSnapshot(station_id='%s', latitude='%s', 
            longitude='%s', weather='%s', temperature_fahrenheit='%s',
            temperature_celsius='%s', feels_like_fahrenheit='%s',
            feels_like_celsius='%s', wind_direction='%s', wind_degrees='%s',
            wind_mph='%s', wind_kph='%s', wind_gust_mph='%s',
            wind_gust_kph='%s', relative_humidity='%s', precipitation_in='%s',
            precipitation_mm='%s', dewpoint_celsius='%s', visibility_mi='%s', 
            visibility_km='%s', uv='%s')>''' % (self.station_id, self.latitude,
                                                self.longitude, self.weather,
                                                self.temperature_fahrenheit,
                                                self.temperature_celsius,
                                                self.feels_like_fahrenheit,
                                                self.feels_like_celsius,
                                                self.wind_direction,
                                                self.wind_degrees,
                                                self.wind_mph, self.wind_kph,
                                                self.wind_gust_mph,
                                                self.wind_gust_kph,
                                                self.relative_humidity,
                                                self.precipitation_in,
                                                self.precipitation_mm,
                                                self.dewpoint_celsius,
                                                self.visibility_mi,
                                                self.visibility_km, self.uv)
