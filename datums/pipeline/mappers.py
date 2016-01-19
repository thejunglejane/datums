import uuid
from dateutil.parser import parse
from datums import models


_model_type_mapper = {
    'altitude': models.AltitudeReport,
    'audio': models.AudioReport,
    'location': models.LocationReport,
    'placemark': models.PlacemarkReport,
    'report': models.Report,
    'weather': models.WeatherReport
}

_key_type_mapper = {
    'date': parse,
    'draft': bool,
    'timestamp': parse,
    'uniqueIdentifier': uuid.UUID
}

# TODO (jsa): just snakeify Reporter's attribute names and call it a day, other-
# wise datums will break every time Reporter updates attributes
_report_key_mapper = {
    'altitude': {
        'adjustedPressure': 'pressure_adjusted',
        'floorsAscended': 'floors_ascended',
        'floorsDescended': 'floors_descended',
        'gpsAltitudeFromLocation': 'gps_altitude_from_location',
        'gpsRawAltitude': 'gps_altitude_raw',
        'pressure': 'pressure',
        'reportUniqueIdentifier': 'report_id',  # added
        'uniqueIdentifier': 'id'
    },
    'audio': {
        'avg': 'average',
        'peak': 'peak',
        'reportUniqueIdentifier': 'report_id',  # added
        'uniqueIdentifier': 'id'
    },
    'background': 'background',
    'battery': 'battery',
    'connection': 'connection',
    'date': 'created_at',
    'draft': 'draft',
    'location': {
        'altitude': 'altitude',
        'course': 'course',
        'horizontalAccuracy': 'horizontal_accuracy',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'placemark': {
            # TODO (jsa): don't assume U.S. addresses
            'administrativeArea': 'state',
            'country': 'country',
            'inlandWater': 'inland_water',
            'locality': 'city',
            'locationUniqueIdentifier': 'location_report_id',  # added
            'name': 'address',
            'postalCode': 'postal_code',
            'region': 'region',
            'subAdministrativeArea': 'county',
            'subLocality': 'neighborhood',
            'subThoroughfare': 'street_number',
            'thoroughfare': 'street_name',
            'uniqueIdentifier': 'id'
        },
        'reportUniqueIdentifier': 'report_id',  # added
        'speed': 'speed',
        'timestamp': 'created_at',
        'uniqueIdentifier': 'id',
        'verticalAccuracy': 'vertical_accuracy'
    },
    'reportImpetus': 'report_impetus',
    'sectionIdentifier': 'section_identifier',
    'steps': 'steps',
    'uniqueIdentifier': 'id',
    'weather': {
        'dewpointC': 'dewpoint_celsius',
        'feelslikeC': 'feels_like_celsius',
        'feelslikeF': 'feels_like_fahrenheit',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'precipTodayIn': 'precipitation_in',
        'precipTodayMetric': 'precipitation_mm',
        'pressureIn': 'pressure_in',
        'pressureMb': 'pressure_mb',
        'relativeHumidity': 'relative_humidity',
        'reportUniqueIdentifier': 'report_id',  # added
        'stationID': 'station_id',
        'tempC': 'temperature_celsius',
        'tempF': 'temperature_fahrenheit',
        'uniqueIdentifier': 'id',
        'uv': 'uv',
        'visibilityKM': 'visibility_km',
        'visibilityMi': 'visibility_mi',
        'weather': 'weather',
        'windDegrees': 'wind_degrees',
        'windDirection': 'wind_direction',
        'windGustKPH': 'wind_gust_kph',
        'windGustMPH': 'wind_gust_mph',
        'windKPH': 'wind_kph',
        'windMPH': 'wind_mph'
    }
}
