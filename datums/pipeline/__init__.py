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


def _traverse_report(report, action, key_mapper=mappers._report_key_mapper):
    '''Return the dictionary of **kwargs based on the report and the action
    specified.
    '''
    _top_level = [key for key in report if not isinstance(report[key], dict)]
    # Set aside nested reports for recursion
    _nested_level = [key for key in report if isinstance(report[key], dict)]
    top_level_dict = {}
    nested_level_dict = {}
    for key in _top_level:
        try:
            item = mappers._key_type_mapper[key](
                str(report[key]) if key != 'draft' else report[key])
        except KeyError:
            item = report[key]
        finally:
            top_level_dict[key_mapper[key]] = item
    for key in _nested_level:
        try:
            nested_level_dict[key] = mappers._key_type_mapper[key](
                str(report[key]) if key != 'draft' else report[key])
        except KeyError:
            nested_level_dict[key] = report[key]
        nested_level_dict[key][
            'reportUniqueIdentifier'] = mappers._key_type_mapper[
                'uniqueIdentifier'](report['uniqueIdentifier'])
        if key == 'placemark':
            # Add the parent location report UUID
            nested_level_dict[key][
                'locationUniqueIdentifier'] = nested_level_dict[key].pop(
                    'reportUniqueIdentifier')
        elif key == 'altitude':
            try:
                nested_level_dict[key]['uniqueIdentifier'] = report[key][
                    'uniqueIdentifier']
            except KeyError:  # not all altitude reports have a UUID
                if action == 'get_or_create':
                    nested_level_dict[key]['uniqueIdentifier'] = uuid.uuid4()
                else:
                    warnings.warn('''
                        No uniqueIdentifier found for AltitudeReport in {0}.
                        Existing altitude report will not be updated.
                        '''.format(report['uniqueIdentifier']))
                    del nested_level_dict[key]
    return top_level_dict, nested_level_dict


def _report_add(
        report, type=models.Report, key_mapper=mappers._report_key_mapper):
    top_level_report, nested_report = _traverse_report(
        report, 'get_or_create', key_mapper)
    type.get_or_create(**top_level_report)
    for key in nested_report:
        try:
            nested_key_mapper = mappers._report_key_mapper[key]
        except KeyError:
            nested_key_mapper = mappers._report_key_mapper['location'][key]
        _report_add(
            nested_report[key], mappers._model_type_mapper[key], nested_key_mapper)


def _report_update(
        report, type=models.Report, key_mapper=mappers._report_key_mapper):
    top_level_report, nested_report = _traverse_report(
        report, 'update', key_mapper)
    type.update(**top_level_report)
    for key in nested_report:
        try:
            nested_key_mapper = mappers._report_key_mapper[key]
        except KeyError:
            nested_key_mapper = mappers._report_key_mapper['location'][key]
        _report_update(
            nested_report[key], mappers._model_type_mapper[key], nested_key_mapper)


def add_question(question):
    _question(question, models.Question.get_or_create)


def add_snapshot(snapshot):
    report, responses, photoset = _prepare_snapshot(snapshot)
    _report_add(report)
    for response in responses:
        accessor, ids = codec.get_response_accessor(response, report)
        _response(response, accessor.get_or_create_from_legacy_response, **ids)


def update_question(question):
    _question(question, models.Question.update)


def update_snapshot(snapshot):
    report, responses, photoset = _prepare_snapshot(snapshot)
    _report_update(report)
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
