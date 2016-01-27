# -*- coding: utf-8 -*-

import codec
import json
import mappers
import uuid
import warnings
from datums import models

__all__ = ['codec', 'mappers']


def _traverse_report():
    pass


class QuestionPipeline(object):

    def __init__(self, question):
        self.question = question

        self.question_dict = {'type': self.question['questionType'],
                              'prompt': self.question['prompt']}

    def add(self):
        models.Question.get_or_create(**self.question_dict)

    def update(self):
        models.Question.update(**self.question_dict)

    def delete(self):
        models.Question.delete(**self.question_dict)


class ResponsePipeline(object):

    def __init__(self, response, report):
        self.response = response
        self.report = report

        self.accessor, self.ids = codec.get_response_accessor(
            self.response, self.report)

    def add(self):
        self.accessor.get_or_create_from_legacy_response(
            self.response, **self.ids)

    def update(self):
        self.accessor.update(self.response, **self.ids)

    def delete(self):
        self.accessor.delete(self.response, **self.ids)


class ReportPipeline(object):

    def __init__(self, report):
        self.report = report

    def _report(self, action, key_mapper=mappers._report_key_mapper):
        '''Return the dictionary of **kwargs with the correct datums attribute
        names and data types for the top level of the report, and return the
        nested levels separately.
        '''
        _top_level = [
            k for k, v in self.report.items() if not isinstance(v, dict)]
        _nested_level = [
            k for k, v in self.report.items() if isinstance(v, dict)]
        top_level_dict = {}
        nested_levels_dict = {}
        for key in _top_level:
            try:
<<<<<<< HEAD
                if key == 'date':
                    item = mappers._key_type_mapper[key](
                        str(self.report[key]), **{'ignoretz': True})
                elif key == 'draft':
                    item = mappers._key_type_mapper[key](self.report[key])
                else:
                    item = mappers._key_type_mapper[key](str(self.report[key]))
=======
                if key == 'date' or key == 'timestamp':
                    item = mappers._key_type_mapper[key](
                        str(self.report[key]), **{'ignoretz': True})
                else:
                    item = mappers._key_type_mapper[key](str(
                        self.report[key]) if key != 'draft' else self.report[key])
>>>>>>> 5db6c596e670f6f9d15720871ccc0ddba1edc58d
            except KeyError:
                item = self.report[key]
            finally:
                try:
                    top_level_dict[key_mapper[key]] = item
                except KeyError:
                    warnings.warn('''
                        {0} is not currently supported by datums and will be ignored.
                        Would you consider submitting an issue to add support?
                        https://www.github.com/thejunglejane/datums/issues
                        '''.format(key))
        for key in _nested_level:
            nested_levels_dict[key] = self.report[key]
            # Add the parent report ID
            nested_levels_dict[key][
                'reportUniqueIdentifier'] = mappers._key_type_mapper[
                    'uniqueIdentifier'](str(self.report['uniqueIdentifier']))
            if key == 'placemark':
                # Add the parent location report UUID
                nested_levels_dict[key][
                    'locationUniqueIdentifier'] = nested_levels_dict[key].pop(
                        'reportUniqueIdentifier')
            # Create UUID for altitude report if there is not one and the action
            # is get_or_create, else delete the altitude report from the nested
            # levels and warn that it will not be updated
            if 'uniqueIdentifier' not in nested_levels_dict[key]:
                if action.__func__.func_name == 'get_or_create':
                    nested_levels_dict[key]['uniqueIdentifier'] = uuid.uuid4()
                else:
                    del nested_levels_dict[key]
                    warnings.warn('''
                        No uniqueIdentifier found for AltitudeReport in {0}.
                        Existing altitude report will not be updated.
                        '''.format(self.report['uniqueIdentifier']))
        return top_level_dict, nested_levels_dict

    def add(self, action=models.Report.get_or_create,
            key_mapper=mappers._report_key_mapper):
        top_level, nested_levels = self._report(action, key_mapper)
        action(**top_level)
        for nested_level in nested_levels:
            try:
                key_mapper = mappers._report_key_mapper[nested_level]
            except KeyError:
                key_mapper = mappers._report_key_mapper[
                    'location'][nested_level]
            ReportPipeline(nested_levels[nested_level]).add(
                mappers._model_type_mapper[
                    nested_level].get_or_create, key_mapper)

    def update(self, action=models.Report.update,
               key_mapper=mappers._report_key_mapper):
        top_level, nested_levels = self._report(action, key_mapper)
        action(**top_level)
        for nested_level in nested_levels:
            try:
                key_mapper = mappers._report_key_mapper[nested_level]
            except KeyError:
                key_mapper = mappers._report_key_mapper[
                    'location'][nested_level]
            ReportPipeline(nested_levels[nested_level]).update(
                mappers._model_type_mapper[nested_level].update, key_mapper)

    def delete(self):
        models.Report.delete(**{'id': mappers._key_type_mapper[
            'uniqueIdentifier'](str(self.report['uniqueIdentifier']))})


class SnapshotPipeline(object):

    def __init__(self, snapshot):
        self.snapshot = snapshot

        self.report = self.snapshot.copy()
        self.responses = self.report.pop('responses')

        _ = self.report.pop('photoSet', None)  # TODO (jsa): add support

    def add(self):
        ReportPipeline(self.report).add()
        for response in self.responses:
            ResponsePipeline(response, self.report).add()

    def update(self):
        ReportPipeline(self.report).update()
        for response in self.responses:
            ResponsePipeline(response, self.report).update()

    def delete(self):
        ReportPipeline(self.report).delete()
