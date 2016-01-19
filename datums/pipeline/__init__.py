# -*- coding: utf-8 -*-

import codec
import json
import mappers
import uuid
import warnings
from datums import models

__all__ = ['codec', 'mapers']


def _prepare_snapshot(snapshot):
    report = snapshot.copy()
    responses = report.pop('responses', None)
    photoset = report.pop('photoSet', None)  # TODO (jsa): add support
    return report, responses, photoset


def _question(question, action):
    '''Perform the action specified (models.Question.get_or_create,
    models.Question.update, or models.Question.delete) on the question.
    '''
    question_dict = {'type': question['questionType'],
                     'prompt': question['prompt']}
    action(**question_dict)


def _response(response, action, **kwargs):
    '''Perform the action specified
    (models.Response.get_or_create_from_legacy_response, models.Response.update,
    or models.Response.delete) on the response.
    '''
    action(response, **kwargs)


def _report(report, type, action, key_mapper=mappers._report_key_mapper):
    '''Perform the action specified (get_or_create, update, or delete) on the
    report.
    '''
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
                try:
                    reports_nested[key]['uniqueIdentifier'] = report[key][
                        'uniqueIdentifier']
                except KeyError:  # not all altitude reports have a UUID
                    if action.__func__.func_name == 'get_or_create':
                        reports_nested[key]['uniqueIdentifier'] = uuid.uuid4()
                    else:
                        warnings.warn('''
                            No uniqueIdentifier found for altitude report in {0}.
                            Existing altitude report will not be updated or deleted.
                            '''.format(report['uniqueIdentifier']))
        else:
            try:
                item = mappers._key_type_mapper[key](
                    str(report[key]) if key != 'draft' else report[key])
            except KeyError:
                item = report[key]
            finally:
                reports_dict[key_mapper[key]] = item
    # TODO (jsa): get_or_create, update, and delete take different args
    action(**reports_dict)
    # Recurse nested reports
    for key in reports_nested:
        _report(report[key], key, action=getattr(
            mappers._model_type_mapper[key], action.__func__.func_name), key_mapper=key_mapper[key])


def add_question(question):
    _question(question, models.Question.get_or_create)


def add_snapshot(snapshot):
    report, responses, photoset = _prepare_snapshot(snapshot)
    _report(report, 'report', models.Report.get_or_create)
    for response in responses:
        accessor, ids = codec.get_response_accessor(response, report)
        _response(response, accessor.get_or_create_from_legacy_response, **ids)


def update_question(question):
    _question(question, models.Question.update)


def update_snapshot(snapshot):
    report, responses, photoset = _prepare_snapshot(snapshot)
    _report(report, 'report', models.Report.update)
    for response in responses:
        accessor, ids = codec.get_response_accessor(response, report)
        _response(response, accessor.update, **ids)


def delete_question(question):
    _question(question, models.Question.delete)


def delete_snapshot(snapshot):
    # Deleting a report cascades to all nested reports and associated responses,
    # so only the top-level report needs to be deleted
    report, responses, photoset = _prepare_snapshot(snapshot)
    models.Report.delete(**{
        mappers._report_key_mapper['uniqueIdentifier']: mappers._key_type_mapper[
            'uniqueIdentifier'](str(report['uniqueIdentifier']))})
