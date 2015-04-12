import json

from datums import models
import codec


def delete_question(question):
    question_dict = {'type': question['questionType'],
                     'prompt': question['prompt']}
    models.Question.delete(**question_dict)


def delete_snapshot(snapshot):
    ids = {'id': snapshot['uniqueIdentifier']}
    models.Snapshot.delete(**ids)


def delete_audio_snapshot(snapshot):
    ids = {'id': snapshot['audio']['uniqueIdentifier']}
    models.AudioSnapshot.delete(**ids)


def delete_location_snapshot(snapshot):
    ids = {'id': snapshot['location']['uniqueIdentifier']}
    models.LocationSnapshot.delete(**ids)


def delete_placemark_snapshot(snapshot):
    ids = {'id': snapshot['location']['placemark']['uniqueIdentifier']}
    models.PlacemarkSnapshot.delete(**ids)


def delete_weather_snapshot(snapshot):
    ids = {'id': snapshot['weather']['uniqueIdentifier']}
    models.WeatherSnapshot.delete(**ids)


def delete_response(response, snapshot):
    accessor, ids = codec.get_response_accessor(response, snapshot)
    accessor.delete(response, **ids)


def delete_report(snapshot):
    # Delete snapshots
    delete_snapshot(snapshot)
    delete_audio_snapshot(snapshot)
    delete_location_snapshot(snapshot)
    delete_placemark_snapshot(snapshot)
    delete_weather_snapshot(snapshot)
    # Delete responses
    for response in snapshot['responses']:
        delete_response(response, snapshot)
