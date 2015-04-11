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
    print 'Snapshot: ', ids['snapshot_id'], '---> Question: ', ids['question_id']
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


def bulk_delete_reports(files):
    if not isinstance(files, list):
        files = [files]
    # Delete all reports in each file in files
    for file in files:
        with open(file, 'r') as f:
            file_day = json.load(f)
        # Delete snapshots for that day
        for snapshot in file_day['snapshots']:
            delete_report(snapshot)
    # Delete all questions in each file in files
    for file in files:
        with open(file, 'r') as f:
            file_day = json.load(f)
        # Delete questions for that day
        for question in file_day['questions']:
            delete_question(question)
