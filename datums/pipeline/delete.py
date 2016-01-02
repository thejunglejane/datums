import json

from datums import models
import codec


models = [models.Snapshot, models.AudioSnapshot, models.LocationSnapshot,
          models.PlacemarkSnapshot, models.WeatherSnapshot]


def delete_snapshot(snapshot, model):
    target = model.__name__.lower().strip('snapshot')
    try:
        ids = {'id': snapshot[target]['uniqueIdentifier']}
    except KeyError:
        if target == '':
            ids = {'id': snapshot['uniqueIdentifier']}
        elif target == 'placemark':
            try:
                ids = {'id': snapshot.get(
                    'location')['placemark']['uniqueIdentifier']}
            except KeyError:
                pass
    else:
        model.delete(**ids)


def delete_question(question):
    question_dict = {'type': question['questionType'],
                     'prompt': question['prompt']}
    models.Question.delete(**question_dict)


def delete_response(response, snapshot):
    accessor, ids = codec.get_response_accessor(response, snapshot)
    accessor.delete(response, **ids)


def delete_report(snapshot):
    # Delete snapshots
    for model in models:
        delete_snapshot(snapshot, model)
    # Delete responses
    for response in snapshot['responses']:
        delete_response(response, snapshot)
