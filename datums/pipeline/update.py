import json

from datums import models
import codec


def update_question(question):
    ids = {'type': question['questionType'],
           'prompt': question['prompt']}
    models.Question.update(question, **ids)


def update_snapshot(snapshot):
    ids = {'id': snapshot['uniqueIdentifier']}
    models.Snapshot.update(snapshot, **ids)


def update_audio_snapshot(snapshot):
    ids = {'id': snapshot['audio']['uniqueIdentifier']}
    models.AudioSnapshot.update(snapshot, **ids)


def update_location_snapshot(snapshot):
    ids = {'id': snapshot['location']['uniqueIdentifier']}
    models.LocationSnapshot.update(snapshot, **ids)


def update_placemark_snapshot(snapshot):
    ids = {'id': snapshot['location']['placemark']['uniqueIdentifier']}
    models.PlacemarkSnapshot.update(snapshot, **ids)


def update_weather_snapshot(snapshot):
    ids = {'id': snapshot['weather']['uniqueIdentifier']}
    models.WeatherSnapshot.update(snapshot, **ids)


def update_response(response, snapshot):
    accessor, ids = codec.get_response_accessor(response, snapshot)
    print 'Snapshot: ', ids['snapshot_id'], '---> Question: ', ids['question_id']
    accessor.update(response, **ids)


def update_report(snapshot):
    # Update snapshots
    update_snapshot(snapshot)
    update_audio_snapshot(snapshot)
    update_location_snapshot(snapshot)
    update_placemark_snapshot(snapshot)
    update_weather_snapshot(snapshot)
    # Update response
    for response in snapshot['responses']:
        update_response(response, snapshot)


def bulk_update_reports(files):
    if not isinstance(files, list):
        files = [files]
    # Update all questions and reports for the files in files
    for file in files:
        with open(file, 'r') as f:
            report = json.load(f)
        # Update questions
        for question in report['questions']:
            update_question(question)
        for snapshot in report['snapshots']:
            update_report(snapshot)
