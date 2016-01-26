# -*- coding: utf-8 -*-

import mock
import random
import unittest
from datums import models
from sqlalchemy.orm import query


class TestModelsBase(unittest.TestCase):

    def setUp(self):
        self.GhostBaseInstance = models.base.GhostBase()

    def tearDown(self):
        del self.GhostBaseInstance

    @mock.patch.object(models.base.metadata, 'create_all')
    def test_database_setup(self, mock_create_all):
        models.base.database_setup(models.engine)
        mock_create_all.assert_called_once_with(models.engine)

    @mock.patch.object(models.base.metadata, 'drop_all')
    def test_database_teardown(self, mock_drop_all):
        models.base.database_teardown(models.engine)
        mock_drop_all.assert_called_once_with(models.engine)

    @mock.patch.object(models.session, 'commit')
    @mock.patch.object(models.session, 'add')
    def test_action_and_commit_valid_kwargs(
            self, mock_session_add, mock_session_commit):
        '''Does the _action_and_commit() method commit the session if the
        kwargs are valid?
        '''
        kwargs = {'section_identifier': 'bar'}
        obj = models.Report(**kwargs)
        setattr(self.GhostBaseInstance, 'section_identifier', 'bar')
        models.base._action_and_commit(obj, mock_session_add)
        mock_session_add.assert_called_once_with(obj)
        self.assertTrue(mock_session_commit.called)


@mock.patch.object(query.Query, 'first')
@mock.patch.object(query.Query, 'filter_by', return_value=query.Query(
    models.Report))
@mock.patch.object(models.session, 'query', return_value=query.Query(
    models.Report))
class TestGhostBase(unittest.TestCase):

    def setUp(self):
        self.GhostBaseInstance = models.base.GhostBase()

    def tearDown(self):
        del self.GhostBaseInstance

    def test_get_instance_exists(
            self, mock_session_query, mock_query_filter, mock_query_first):
        '''Does the _get_instance() method return an existing instance of the
        class?
        '''
        mock_query_first.return_value = models.base.GhostBase()
        self.assertIsInstance(
            self.GhostBaseInstance._get_instance(
                **{'foo': 'bar'}), self.GhostBaseInstance.__class__)
        mock_session_query.assert_called_once_with(models.base.GhostBase)
        mock_query_filter.assert_called_once_with(**{'foo': 'bar'})
        self.assertTrue(mock_query_first.called)

    def test_get_instance_does_not_exist(
            self, mock_session_query, mock_query_filter, mock_query_first):
        '''Does the _get_instance() method return None if no instance of the 
        class exists?
        '''
        mock_query_first.return_value = None
        self.assertIsNone(
            self.GhostBaseInstance._get_instance(**{'foo': 'bar'}))
        mock_session_query.assert_called_once_with(models.base.GhostBase)
        mock_query_filter.assert_called_once_with(**{'foo': 'bar'})
        self.assertTrue(mock_query_first.called)

    @mock.patch.object(models.session, 'add')
    def test_get_or_create_get(self, mock_session_add, mock_session_query,
                               mock_query_filter, mock_query_first):
        '''Does the get_or_create() method return an instance of the class
        without adding it to the session if the instance already exists?
        '''
        mock_query_first.return_value = True
        self.assertTrue(self.GhostBaseInstance.get_or_create(**{'id': 'foo'}))
        mock_session_add.assert_not_called()

    @mock.patch.object(models.session, 'add')
    def test_get_or_create_add(self, mock_session_add, mock_session_query,
                               mock_query_filter, mock_query_first):
        '''Does the get_or_create() method create a new instance and add it to
        the session if the instance does not already exist?
        '''
        mock_query_first.return_value = None
        self.assertIsInstance(
            models.Report.get_or_create(
                **{'id': 'foo'}), models.base.GhostBase)
        self.assertTrue(mock_session_add.called)

    @mock.patch.object(models.session, 'add')
    def test_update_exists(self, mock_session_add, mock_session_query,
                           mock_query_filter, mock_query_first):
        '''Does the update() method update the __dict__ attribute of an
        existing instance of the class and add it to the session?
        '''
        _ = models.Report
        mock_query_first.return_value = _
        self.GhostBaseInstance.update(**{'id': 'bar'})
        self.assertTrue(hasattr(_, 'id'))
        self.assertTrue(mock_session_add.called)

    @mock.patch.object(models.session, 'add')
    def test_update_does_not_exist(self, mock_session_add, mock_session_query,
                                   mock_query_filter, mock_query_first):
        '''Does the update() method create a new instance and add it to the
        session if the instance does not already exist?
        '''
        mock_query_first.return_value = None
        models.Report.update(**{'id': 'bar'})
        self.assertTrue(mock_session_add.called)

    @mock.patch.object(models.base, '_action_and_commit')
    @mock.patch.object(models.session, 'delete')
    def test_delete_exists(
            self, mock_session_delete, mock_action_commit,
            mock_session_query, mock_query_filter, mock_query_first):
        '''Does the delete() method validate an existing instance of the class
        before deleting from the session?
        '''
        mock_query_first.return_value = True
        self.GhostBaseInstance.delete()
        self.assertTrue(mock_action_commit.called)

    @mock.patch.object(models.base, '_action_and_commit')
    @mock.patch.object(models.session, 'delete')
    def test_delete_does_not_exist(
            self, mock_session_delete, mock_action_commit,
            mock_session_query, mock_query_filter, mock_query_first):
        '''Does the delete() method do nothing if the instance does not already
        exists?
        '''
        mock_query_first.return_value = None
        self.GhostBaseInstance.delete()
        mock_action_commit.assert_not_called()


@mock.patch.object(models.base, '_action_and_commit')
class TestResponseClassLegacyAccessor(unittest.TestCase):

    _response_classes = models.Response.__subclasses__()
    _response_classes.remove(models.LocationResponse)  # tested separately

    def setUp(self, mock_response=random.choice(_response_classes)):
        self.LegacyInstance = models.base.ResponseClassLegacyAccessor(
            response_class=mock_response, column='foo_response',
            accessor=(lambda x: x.get('foo')))
        self.test_response = {'foo': 'bar'}
        self.mock_response = mock_response

    def tearDown(self):
        del self.LegacyInstance

    @mock.patch.object(models.base.ResponseClassLegacyAccessor, '_get_instance')
    @mock.patch.object(models.base.ResponseClassLegacyAccessor,
                       'get_or_create_from_legacy_response')
    def test_update_exists(
            self, mock_get_create, mock_get_instance, mock_action_commit):
        '''Does the update() method call _confirm_or_add_response() if there
        isn't an existing instance in the database, without calling
        get_or_create_from_legacy_response()?
        '''
        _ = models.Report()
        mock_get_instance.return_value = _
        self.LegacyInstance.update(self.test_response)
        self.assertTrue(mock_get_instance.called)
        mock_action_commit.assert_called_once_with(_, models.session.add)
        mock_get_create.assert_not_called()

    @mock.patch.object(models.base.ResponseClassLegacyAccessor, '_get_instance')
    @mock.patch.object(models.base.ResponseClassLegacyAccessor,
                       'get_or_create_from_legacy_response')
    def test_update_does_not_exist(
            self, mock_get_create, mock_get_instance, mock_action_commit):
        '''Does the update() method call get_or_create_from_legacy_response()
        if there isn't an existing instance in the database, without calling
        _action_and_commit()?
        '''
        mock_get_instance.return_value = None
        self.LegacyInstance.update(self.test_response)
        mock_action_commit.assert_not_called()
        mock_get_create.assert_called_once_with(self.test_response)

    @mock.patch.object(models.base.ResponseClassLegacyAccessor, '_get_instance')
    def test_delete_exists(self, mock_get_instance, mock_action_commit):
        '''Does the delete() method call _action_and_commit() with
        models.session.delete if an instance exists?
        '''
        _ = models.Report()
        mock_get_instance.return_value = _
        self.LegacyInstance.delete(self.test_response)
        self.assertTrue(mock_get_instance.called)
        mock_action_commit.assert_called_once_with(_, models.session.delete)

    @mock.patch.object(models.base.ResponseClassLegacyAccessor, '_get_instance')
    def test_delete_does_not_exist(
            self, mock_get_instance, mock_action_commit):
        '''Does the delete() method do nothing if no instance exists?
        '''
        mock_get_instance.return_value = None
        self.LegacyInstance.delete(self.test_response)
        self.assertTrue(mock_get_instance.called)
        mock_action_commit.assert_not_called()
