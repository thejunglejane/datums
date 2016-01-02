import json

from datums import models
import codec


models = [models.Snapshot, models.AudioSnapshot, models.LocationSnapshot,
          models.PlacemarkSnapshot, models.WeatherSnapshot]


def update_snapshot(snapshot, model):
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
        model.update(snapshot, **ids)


def update_question(question):
    question_dict = {'type': question['questionType'],
                     'prompt': question['prompt']}
    models.Question.update(question, **question_dict)


def update_response(response, snapshot):
    accessor, ids = codec.get_response_accessor(response, snapshot)
    accessor.update(response, **ids)


def update_report(snapshot):
    # Update snapshots
    for model in models:
        update_snapshot(snapshot, model)
    # Update response
    for response in snapshot['responses']:
        update_response(response, snapshot)
