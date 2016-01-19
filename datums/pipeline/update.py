# -*- coding: utf-8 -*-

import codec
import json
import mappers
import warnings
from datums import models


def update_question(question):
    question_dict = {'type': question['questionType'],
                     'prompt': question['prompt']}
    models.Question.update(question, **question_dict)


def _update_response(response, report):
    accessor, ids = codec.get_response_accessor(response, report)
    accessor.update(response, **ids)


def _update_report(report, type, key_mapper=mappers._report_key_mapper):
    reports_dict = {}
    reports_nested = {}
    # Set aside nested reports for recursion
    for key in report:
        if isinstance(report[key], dict):
            try:
                reports_nested[key] = mappers._key_type_mapper[key](
                    str(report[key]) if key != 'draft' else report[key])
            except KeyError:
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
                try:
                    reports_nested[key]['uniqueIdentifier'] = report[key][
                        'uniqueIdentifier']
                except KeyError:
                    warnings.warn(
                        'No uniqueIdentifier found for altitude report in {0}\
                        Altitude report will not be updated.'.format(
                            report['uniqueIdentifier']))
        else:
            try:
                item = mappers._key_type_mapper[key](
                    str(report[key]) if key != 'draft' else report[key])
            except KeyError:
                item = report[key]
            finally:
                reports_dict[key_mapper[key]] = item
    mappers._model_type_mapper[type].update(report, **reports_dict)
    # Recurse nested reports
    for key in reports_nested:
        _update_report(report[key], type=key, key_mapper=key_mapper[key])


def update_snapshot(snapshot):
    report = snapshot.copy()
    responses = report.pop('responses', None)
    photoset = report.pop('photoSet', None)  # TODO (jsa): add support
    # Update snapshots
    _update_report(report, 'report')
    # Update response
    for response in responses:
        _update_response(response, report)
