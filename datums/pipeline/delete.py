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


def _delete_report(report, type, key_mapper=mappers._report_key_mapper):
    # Deleting a report cascades to all nested reports and associated responses,
    # so only the top-level report needs to be deleted
    mappers._model_type_mapper[type].delete(**{
        key_mapper['uniqueIdentifier'] : mappers._key_type_mapper[
            'uniqueIdentifier'](str(report['uniqueIdentifier']))})


def delete_snapshot(snapshot):
    report = snapshot.copy()
    responses = report.pop('responses')
    photoset = report.pop('photoSet', None)  # TODO (jsa): add support
    # Delete snapshots
    _delete_report(report, 'report')
