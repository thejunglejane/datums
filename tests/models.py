from datums import models
from functools import wraps
from sqlalchemy.orm import query
import mock
import unittest


# TODO (jsa): wrap assertions that are common to all test methods
# self.assertTrue(mock_query_first.called)
# self.assertTrue(mock_query_filter_by.called)
# self.assertTrue(mock_session_query.called)


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

    @mock.patch.object(models.session, 'add')
    def test_get_or_create_get(self, mock_session_add, mock_session_query,
                               mock_query_filter_by, mock_query_first):
        '''Does the get_or_create() method return an instance of the class
        without adding it to the session if the instance already exists?
        '''
        mock_query_first.return_value = True
        self.assertTrue(self.GhostBaseInstance.get_or_create())
        self.assertTrue(mock_query_first.called)
        self.assertTrue(mock_query_filter_by.called)
        self.assertTrue(mock_session_query.called)
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
        self.assertTrue(mock_query_first.called)
        self.assertTrue(mock_query_filter_by.called)
        self.assertTrue(mock_session_query.called)
        self.assertTrue(mock_session_add.called)

    @mock.patch.object(models.session, 'add')
    def test_update_exists(self, mock_session_add, mock_session_query,
                           mock_query_filter_by, mock_query_first):
        '''Does the update() method update the __dict__ attribute of an
        existing instance of the class and add it to the session?
        '''
        mock_query_first.return_value = models.Snapshot
        self.GhostBaseInstance.update(snapshot={'foo': 'bar'})
        self.assertTrue(mock_query_first.called)
        self.assertTrue(mock_query_filter_by.called)
        self.assertTrue(mock_session_query.called)
        self.assertTrue(mock_session_add.called)

    @mock.patch.object(models.session, 'add')
    def test_update_does_not_exist(self, mock_session_add, mock_session_query,
                                   mock_query_filter_by, mock_query_first):
        '''Does the update() method create a new instance and add it to the
        session if the instance does not already exist?
        '''
        mock_query_first.return_value = None
        self.GhostBaseInstance.update(snapshot={'foo': 'bar'})
        self.assertTrue(mock_query_first.called)
        self.assertTrue(mock_query_filter_by.called)
        self.assertTrue(mock_session_query.called)
        self.assertTrue(mock_session_add.called)

    @mock.patch.object(models.session, 'delete')
    def test_delete_exists(self, mock_session_delete, mock_session_query,
                           mock_query_filter_by, mock_query_first):
        '''Does the delete() method delete an existing instance of the class
        from the session?
        '''
        mock_query_first.return_value = True
        self.GhostBaseInstance.delete()
        self.assertTrue(mock_query_first.called)
        self.assertTrue(mock_query_filter_by.called)
        self.assertTrue(mock_session_query.called)
        self.assertTrue(mock_session_delete.called)

    @mock.patch.object(models.session, 'delete')
    def test_delete_does_not_exist(self, mock_session_delete,
                                   mock_session_query, mock_query_filter_by,
                                   mock_query_first):
        '''Does the delete() method do nothing if the instance does not already
        exists?
        '''
        mock_query_first.return_value = None
        self.GhostBaseInstance.delete()
        self.assertTrue(mock_query_first.called)
        self.assertTrue(mock_query_filter_by.called)
        self.assertTrue(mock_session_query.called)
        mock_session_delete.assert_not_called()
