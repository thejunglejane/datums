import codec
import mappers
from datums import models


def add_question(question):
    question_dict = {'type': question['questionType'],
                     'prompt': question['prompt']}
    models.Question.get_or_create(**question_dict)


def add_response(response, snapshot):
    accessor, ids = codec.get_response_accessor(response, snapshot)
    accessor.get_or_create_from_legacy_response(response, **ids)


def add_snapshot(snapshot, type, key_mapper=mappers._snapshot_key_mapper):
    snapshot_dict = {}
    snapshot_nested = {}
    # Set aside nested snapshots for recursion
    for key in snapshot:
        if isinstance(snapshot[key], dict):
            snapshot_nested[key] = snapshot[key]
            snapshot_nested[key]['snapshotUniqueIdentifier'] = mappers._key_type_mapper[
                'uniqueIdentifier'](snapshot['uniqueIdentifier'])
            if key == 'placemark':
                snapshot_nested[key]['locationUniqueIdentifier'] = snapshot_nested[
                    key].pop('snapshotUniqueIdentifier')
        else:
            try:
                item = mappers._key_type_mapper[key](str(snapshot[key]))
            except KeyError:
                item = snapshot[key]
            finally:
                snapshot_dict[key_mapper[key]] = item
    mappers._model_type_mapper[type].get_or_create(**snapshot_dict)
    # Recurse nested snapshots
    for key in snapshot_nested:
        add_snapshot(snapshot[key], type=key, key_mapper=key_mapper[key])


def add_report(report):
    snapshot = report.copy()
    responses = snapshot.pop('responses')
    add_snapshot(snapshot)
    for response in responses:
        add_response(response, snapshot)
