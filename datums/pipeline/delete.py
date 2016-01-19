# -*- coding: utf-8 -*-

import codec
import json
import mappers
import warnings
from datums import models


def delete_question(question):
    question_dict = {'type': question['questionType'],
                     'prompt': question['prompt']}
    models.Question.delete(**question_dict)


def _delete_response(response, report):
    accessor, ids = codec.get_response_accessor(response, report)
    accessor.delete(response, **ids)


def _delete_report(report, type, key_mapper=mappers._report_key_mapper):
    reports_dict = {}
    reports_nested = {}
    # Set aside nested reports for recursion
    for key in report:
        if isinstance(report[key], dict):
            # Not all altitude reports have a uniqueIdentifier
            try:
                reports_nested[key]['uniqueIdentifier'] = report[key][
                    'uniqueIdentifier']
            except KeyError:
                warnings.warn(
                    'No uniqueIdentifier found for altitude report in {0}\
                    Altitude report will not be deleted.'.format(
                        report['uniqueIdentifier']))
    reports_dict[key_mapper['uniqueIdentifier']] = mappers._key_type_mapper[
        'uniqueIdentifier'](str(report['uniqueIdentifier']))
    mappers._model_type_mapper[type].delete(**reports_dict)
    # Recurse nested reports
    for key in reports_nested:
        _delete_report(report[key], type=key, key_mapper=key_mapper[key])


def delete_snapshot(snapshot):
    report = snapshot.copy()
    responses = report.pop('responses')
    photoset = report.pop('photoSet', None)  # TODO (jsa): add support
    # Delete snapshots
    _delete_report(report, 'report')
    # Delete responses
    for response in responses:
        _delete_response(response, report)
