from dateutil.parser import parse
import json
import re
import uuid

from datums import models


__all__ = ['add', 'codec', 'delete', 'update']


_model_type_mapper = {
    'altitude': models.AltitudeSnapshot,
    'audio': models.AudioSnapshot,
    'location': models.LocationSnapshot,
    'placemark': models.PlacemarkSnapshot,
    'snapshot': models.Snapshot,
    'weather': models.WeatherSnapshot
}

_key_type_mapper = {
    'uniqueIdentifier': uuid.UUID,
    'date': parse,
    'timestamp': parse
}

# Map Reporter attribute names to Datums attribute names
_snapshot_key_mapper = {
    'altitude': {
        'adjusted_pressure': 'pressure_adjusted',
        'floorsAscended': 'floors_ascended',
        'floorsDescended': 'floors_descended',
        'gpsAltitudeFromLocation': 'gps_altitude_from_location',
        'gpsRawAltitude': 'gps_altitude_raw',
        'pressure': 'pressure'
    },
    'audio': {
        'avg': 'average',
        'peak': 'peak',
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
            'locality': 'city',
            'name': 'address',
            'postalCode': 'postal_code',
            'region': 'region',
            'subAdministrativeArea': 'county',
            'subLocality': 'neighborhood',
            'subThoroughfare': 'street_number',
            'thoroughfare': 'street_name',
            'uniqueIdentifier': 'id'
        },
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
        'stationID': 'station_id',
        'temperatureC': 'temperature_celsius',
        'temperatureF': 'temperature_fahrenheit',
        'uniqueIdentifier': 'id',
        'uv': 'uv',
        'visibilityKM': 'visibility_km',
        'visibilityMi': 'visibility_mi',
        'weather': 'weather',
        'windDegrees': 'wind_degrees',
        'windDirection': 'wind_direciton',
        'windGustMPH': 'wind_gust_kph',
        'windGustMPH': 'wind_gust_mph',
        'windKPH': 'wind_kph',
        'windMPH': 'wind_mph'
    }
}
