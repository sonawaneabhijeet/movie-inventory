import unittest
from unittest.mock import patch

from flask_restful import marshal

from flaskr.view.movie_snapshots_view import MovieSnapshotsView
from tests.fixtures.test_client import TestClient


class MovieSnapshotTests(unittest.TestCase):
    __test_client = TestClient.create()

    @patch("flaskr.resource.movie_snapshots.MovieSnapshotsService")
    def test_should_return_Ok_given_a_request_to_get_all_movie_snapshots(self, movie_snapshots_service):
        movie_snapshots_service.return_value.get_all.return_value = []
        response = self.__test_client.get("/movie-snapshots")
        self.assertEqual(200, response.status_code)

    @patch("flaskr.resource.movie_snapshots.MovieSnapshotsService")
    def test_should_return_no_snapshots_given_no_snapshots_exist(self, movie_snapshots_service):
        movie_snapshots_service.return_value.get_all.return_value = []
        response = self.__test_client.get("/movie-snapshots")
        self.assertEqual([], response.json)

    @patch("flaskr.resource.movie_snapshots.MovieSnapshotsService")
    def test_should_assert_total_snapshots_to_equal_1(self, movie_snapshots_service):
        movie_snapshots_service.return_value.get_all.return_value = [{}]
        response = self.__test_client.get("/movie-snapshots")
        movie_snapshots = response.json
        self.assertEqual(len(movie_snapshots), 1)

    @patch("flaskr.resource.movie_snapshots.MovieSnapshotsService")
    def test_should_assert_all_snapshots(self, movie_snapshots_service):
        movie_snapshot_views = [MovieSnapshotsView("3 idiots", "Rajkumar Hirani")]
        expected_movie_snapshots_views = marshal(movie_snapshot_views, fields=MovieSnapshotsView.DISPLAYABLE_FIELDS)
        movie_snapshots_service.return_value.get_all.return_value = expected_movie_snapshots_views

        response = self.__test_client.get("/movie-snapshots")
        actual_movie_snapshot_views = response.json
        self.assertEqual(actual_movie_snapshot_views, expected_movie_snapshots_views)