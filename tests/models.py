# -*- coding: utf-8 -*-

from datums import models
from sqlalchemy.orm import query
import mock
import unittest


@mock.patch.object(query.Query, 'first')
@mock.patch.object(query.Query, 'filter_by', return_value=query.Query(
    models.Snapshot))
@mock.patch.object(models.session, 'query', return_value=query.Query(
    models.Snapshot))
class TestGhostBase(unittest.TestCase):

    def setUp(self):
        self.GhostBaseInstance = models.base.GhostBase()

    def tearDown(self):
        del self.GhostBaseInstance

    def test_get_instance_exists(
            self, mock_session_query, mock_query_filter_by, mock_query_first):
        '''Does the _get_instance() method return an existing instance of the
        class?
        '''
        mock_query_first.return_value = models.base.GhostBase()
        self.assertIsInstance(
            self.GhostBaseInstance._get_instance(
                **{'foo': 'bar'}), self.GhostBaseInstance.__class__)
        mock_session_query.assert_called_once_with(models.base.GhostBase)
        mock_query_filter_by.assert_called_once_with(**{'foo': 'bar'})
        self.assertTrue(mock_query_first.called)

    def test_get_instance_does_not_exist(
            self, mock_session_query, mock_query_filter_by, mock_query_first):
        '''Does the _get_instance() method return None if no instance of the 
        class exists?
        '''
        mock_query_first.return_value = None
        self.assertIsNone(
            self.GhostBaseInstance._get_instance(**{'foo': 'bar'}))
        mock_session_query.assert_called_once_with(models.base.GhostBase)
        mock_query_filter_by.assert_called_once_with(**{'foo': 'bar'})
        self.assertTrue(mock_query_first.called)

    @mock.patch.object(models.session, 'commit')
    @mock.patch.object(models.session, 'add')
    def test_validate_and_commit_valid_kwargs(
            self, mock_session_add, mock_session_commit,
            mock_session_query, mock_query_filter_by, mock_query_first):
        '''Does the _validate_and_commit() method commit the session if the
        **kwargs are valid?
        '''
        kwargs = {'foo': 'bar'}
        obj = models.Snapshot(**kwargs)
        setattr(self.GhostBaseInstance, 'foo', 'bar')
        self.GhostBaseInstance._validate_and_commit(
            obj, mock_session_add, **kwargs)
        mock_session_add.assert_called_once_with(obj)
        self.assertTrue(mock_session_commit.called)
        delattr(self.GhostBaseInstance, 'foo')

    @mock.patch.object(models.session, 'rollback')
    @mock.patch.object(models.session, 'add')
    def test_validate_and_commit_invalid_kwargs(
            self, mock_session_add, mock_session_rollback,
            mock_session_query, mock_query_filter_by, mock_query_first):
        '''Does the _validate_and_commit() method rollback the session if the
        **kwargs are invalid and raise an AssertionError?
        '''
        kwargs = {'foo': 'bar'}
        obj = models.Snapshot(**{'foo': 'baz'})
        setattr(self.GhostBaseInstance, 'foo', 'bar')
        with self.assertRaises(AssertionError):
            self.GhostBaseInstance._validate_and_commit(
                obj, mock_session_add, **kwargs)
        mock_session_add.assert_called_once_with(obj)
        self.assertTrue(mock_session_rollback.called)
        delattr(self.GhostBaseInstance, 'foo')

    @mock.patch.object(models.session, 'add')
    def test_get_or_create_get(self, mock_session_add, mock_session_query,
                               mock_query_filter_by, mock_query_first):
        '''Does the get_or_create() method return an instance of the class
        without adding it to the session if the instance already exists?
        '''
        mock_query_first.return_value = True
        self.assertTrue(self.GhostBaseInstance.get_or_create())
        mock_session_add.assert_not_called()

    @mock.patch.object(models.session, 'add')
    def test_get_or_create_add(self, mock_session_add, mock_session_query,
                               mock_query_filter_by, mock_query_first):
        '''Does the get_or_create() method create a new instance and add it to
        the session if the instance does not already exist?
        '''
        mock_query_first.return_value = None
        self.assertIsInstance(
            self.GhostBaseInstance.get_or_create(), models.base.GhostBase)
        self.assertTrue(mock_session_add.called)

    @mock.patch.object(models.session, 'add')
    def test_update_exists(self, mock_session_add, mock_session_query,
                           mock_query_filter_by, mock_query_first):
        '''Does the update() method update the __dict__ attribute of an
        existing instance of the class and add it to the session?
        '''
        mock_query_first.return_value = models.Snapshot
        self.GhostBaseInstance.update(snapshot={'foo': 'bar'})
        self.assertTrue(mock_session_add.called)

    @mock.patch.object(models.session, 'add')
    def test_update_does_not_exist(self, mock_session_add, mock_session_query,
                                   mock_query_filter_by, mock_query_first):
        '''Does the update() method create a new instance and add it to the
        session if the instance does not already exist?
        '''
        mock_query_first.return_value = None
        self.GhostBaseInstance.update(snapshot={'foo': 'bar'})
        self.assertTrue(mock_session_add.called)

    @mock.patch.object(models.session, 'delete')
    def test_delete_exists(self, mock_session_delete, mock_session_query,
                           mock_query_filter_by, mock_query_first):
        '''Does the delete() method delete an existing instance of the class
        from the session?
        '''
        mock_query_first.return_value = True
        self.GhostBaseInstance.delete()
        self.assertTrue(mock_session_delete.called)

    @mock.patch.object(models.session, 'delete')
    def test_delete_does_not_exist(
            self, mock_session_delete, mock_session_query,
            mock_query_filter_by, mock_query_first):
        '''Does the delete() method do nothing if the instance does not already
        exists?
        '''
        mock_query_first.return_value = None
        self.GhostBaseInstance.delete()
        mock_session_delete.assert_not_called()
class TestModelsBase(unittest.TestCase):

    @mock.patch.object(models.base.metadata, 'create_all')
    def test_database_setup(self, mock_create_all):
        models.base.database_setup(models.engine)
        mock_create_all.assert_called_once_with(models.engine)

    @mock.patch.object(models.base.metadata, 'drop_all')
    def test_database_teardown(self, mock_drop_all):
        models.base.database_teardown(models.engine)
        mock_drop_all.assert_called_once_with(models.engine)
