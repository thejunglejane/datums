from datums import models
from sqlalchemy.orm import query
import mock
import unittest


class TestGhostBase(unittest.TestCase):

    def setUp(self):
        self.GhostBaseInstance = models.base.GhostBase()

    def tearDown(self):
        del self.GhostBaseInstance

    @mock.patch.object(query.Query, 'first', return_value=query.Query(
        models.Snapshot))
    @mock.patch.object(query.Query, 'filter_by', return_value=query.Query(
        models.Snapshot))
    @mock.patch.object(models.session, 'query', return_value=query.Query(
        models.Snapshot))
    @mock.patch.object(models.session, 'add')
    def test_get_or_create_get(self, mock_session_add, mock_session_query,
            mock_query_filter_by, mock_query_first):
        '''Does the get_or_create() method return an instance of the class
        without adding it to the session if the instance already exists?
        '''
        self.GhostBaseInstance.get_or_create()
        self.assertTrue(mock_query_first.called)
        self.assertTrue(mock_query_filter_by.called)
        self.assertTrue(mock_session_query.called)
        mock_session_add.assert_not_called()

    @mock.patch.object(query.Query, 'first', return_value=None)
    @mock.patch.object(query.Query, 'filter_by', return_value=query.Query(
        models.Snapshot))
    @mock.patch.object(models.session, 'query', return_value=query.Query(
        models.Snapshot))
    @mock.patch.object(models.session, 'add')
    def test_get_or_create_add(self, mock_session_add,
            mock_session_query, mock_query_filter_by, mock_query_first):
        '''Does the get_or_create() method create a new instance and add it to
        the session if the instance does not already exists?
        '''
        self.GhostBaseInstance.get_or_create()
        self.assertTrue(mock_query_first.called)
        self.assertTrue(mock_query_filter_by.called)
        self.assertTrue(mock_session_query.called)
        self.assertTrue(mock_session_add.called)
