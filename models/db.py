from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine


'''Create the Reporter database ORM. Note that some information captured by the 
Reporter application are not included (e.g., photo sets).'''

# Initialize database engine
engine = create_engine('postgresql://jsa@localhost:5432/datums',
                       echo=False, pool_size=20, max_overflow=0)

# Initialize declarative base
Base = declarative_base()


class Question(Base):

    '''The questions table is a join table with a question ID, prompt and 
    response type.'''
    __tablename__ = 'questions'

    prompt = Column(String, primary_key=True, nullable=False)
    response_type_id = Column(Integer)
    response_type = Column(String)

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)

    def __repr__(self):
        return '''<Question(prompt='%s', response_type_id='%s', 
            reponse_type='%s')>''' % (self.prompt, self.response_type_id,
                                      self.response_type)


class Response(Base):

    '''The responses table holds the response information of a report. Each
    response is linked to a snapshot and a question id.'''
    __tablename__ = 'responses'

    snapshot_id = Column(
        String, ForeignKey('snapshots.id'), primary_key=True, nullable=False)
    question_prompt = Column(
        String, ForeignKey('questions.prompt'), nullable=False)
    response = Column(String)

    question = relationship(
        'Question', backref=backref('responses'))

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Response(question_prompt='%s', response='%s')>" % (
            self.question_prompt, self.response)


class Snapshot(Base):

    '''The snapshots table holds the non-response information that Reporter 
    collects when a report is made.'''
    __tablename__ = 'snapshots'

    id = Column(String, primary_key=True, nullable=False)
    audio_snapshot_id = Column(
        String, ForeignKey('audio_snapshots.id'), nullable=False)
    location_snapshot_id = Column(
        String, ForeignKey('location_snapshots.id'), nullable=False)
    weather_snapshot_id = Column(
        String, ForeignKey('weather_snapshots.id'), nullable=False)
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

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)

    def __repr__(self):
        return '''<Snapshot(created_at='%s', report_impetus='%s', battery='%s',
            steps='%s', floors_ascended='%s', floors_descended='%s')>''' % (
            self.created_at, self.report_impetus, self.battery, self.steps,
            self.floors_ascended, self.floors_descended)


class AudioSnapshot(Base):
    __tablename__ = 'audio_snapshots'

    id = Column(String, primary_key=True, nullable=False)
    average = Column(Numeric)
    peak = Column(Numeric)

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<AudioSnapshot(average='%s', peak='%s')>" % (self.average,
                                                             self.peak)


class LocationSnapshot(Base):
    __tablename__ = 'location_snapshots'

    id = Column(String, primary_key=True, nullable=False)
    placemark_id = Column(
        String, ForeignKey('placemark_snapshots.id'), nullable=False)
    created_at = Column(DateTime)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    altitude = Column(Numeric)
    speed = Column(Numeric)
    vertical_accuracy = Column(Numeric)
    horizontal_accuracy = Column(Numeric)

    placemark = relationship(
        'PlacemarkSnapshot', backref=backref('location_snapshots', order_by=id))

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)

    def __repr__(self):
        return '''<LocationSnapshot(created_at='%s', latitude='%s',
            longitude='%s', altitude='%s', speed='%s', vertical_accuracy='%s',
            horizontal_accuracy='%s')>''' % (
            self.created_at, self.latitude, self.longitude, self.altitude,
            self.speed, self.vertical_accuracy, self.horizontal_accuracy)


class PlacemarkSnapshot(Base):
    __tablename__ = 'placemark_snapshots'

    id = Column(String, primary_key=True, nullable=False)
    street_address = Column(String)
    neighborhood = Column(String)
    city = Column(String)
    county = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)

    def __repr__(self):
        return '''<PlacemarkSnapshot(street_address='%s', neighborhood='%s', 
            city='%s', county='%s', state='%s', country='%s', 
            postal_code='%s')>''' % (self.street_address, self.neighborhood,
                                     self.city, self.county, self.state,
                                     self.country, self.postal_code)


class WeatherSnapshot(Base):
    __tablename__ = 'weather_snapshots'

    id = Column(String, primary_key=True, nullable=False)
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
    precipitation_mm = Column(Numeric)  # double check that this is mm
    dewpoint_celsius = Column(Numeric)
    visibility_mi = Column(Numeric)
    visibility_km = Column(Numeric)
    uv = Column(Numeric)

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)

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

# Create the tables in the database
Base.metadata.create_all(engine)
