# -*- coding: utf-8 -*-

import codec
import mappers
import uuid
from datums import models


def add_question(question):
    question_dict = {'type': question['questionType'],
                     'prompt': question['prompt']}
    models.Question.get_or_create(**question_dict)


def _add_response(response, report):
    accessor, ids = codec.get_response_accessor(response, report)
    accessor.get_or_create_from_legacy_response(response, **ids)


def _add_report(report, type, key_mapper=mappers._report_key_mapper):
    reports_dict = {}
    reports_nested = {}
    # Set aside nested reports for recursion
    for key in report:
        if isinstance(report[key], dict):
            reports_nested[key] = report[key]
            reports_nested[key][
                'reportUniqueIdentifier'] = mappers._key_type_mapper[
                    'uniqueIdentifier'](report['uniqueIdentifier'])
            if key == 'placemark':
                # Add the parent location report UUID
                reports_nested[key][
                    'locationUniqueIdentifier'] = reports_nested[key].pop(
                        'reportUniqueIdentifier')
            elif key == 'altitude':
                # Not all altitude reports have a uniqueIdentifier
                reports_nested[key]['uniqueIdentifier'] = report[key].get(
                    'uniqueIdentifier', uuid.uuid4())
        else:
            try:
                item = mappers._key_type_mapper[key](str(report[key]))
            except KeyError:
                item = report[key]
            finally:
                reports_dict[key_mapper[key]] = item
    mappers._model_type_mapper[type].get_or_create(**reports_dict)
    # Recurse nested reports
    for key in reports_nested:
        _add_report(report[key], type=key, key_mapper=key_mapper[key])


def add_snapshot(snapshot):
    report = snapshot.copy()
    responses = report.pop('responses', None)
    photoset = report.pop('photoSet', None)  # TODO (jsa): add support
    _add_report(report, 'report')
    for response in responses:
        _add_response(response, report)
