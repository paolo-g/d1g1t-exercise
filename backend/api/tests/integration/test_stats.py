"""Module test_stats providing integration tests for stats endpoint"""
import statistics
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import (
    Team, Happiness
)

class StatsIntegrationTest(APITestCase):
    """
    Tests to cover stats endpoint
    """

    def setUp(self):
        """
        Use the user model django points to
        """
        self.custom_user = get_user_model()

    def create_happiness_report(self,
                                team_name: str,
                                username: str,
                                rating: int) -> get_user_model():
        """
        Helper function that creates a team, user and user happiness report

        :param team_name: The name of the team to create
        :param username: The name of the user to create
        :param rating: The rating of the happiness report to create
        :return: Returns a CustomUser object
        """
        team = Team.objects.create(name=team_name)
        user = self.custom_user.objects.create_user(username=username,
                                                    password='',
                                                    team=team)
        Happiness.objects.create(owner=user,
                                 rating=rating)
        return user

    def test_stats_anon_empty(self):
        """
        Get stats endpoint with no data, anonymously
        """
        response = self.client.get('/stats/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data)

    def test_stats_anon_onereport(self):
        """
        Get stats endpoint with one user happiness report, anonymously
        """
        team_name = 'anon_onereport'
        username = 'anon_onereport'
        rating = 3
        self.create_happiness_report(team_name,
                                     username,
                                     rating)

        response = self.client.get('/stats/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {team_name: rating}
        self.assertEqual(response.data, expected_data)

    def test_stats_anon_tworeports(self):
        """
        Get stats endpoint with two user happiness reports on two teams, anonymously
        """
        first_team = 'anon_tworeports1'
        first_user = 'anon_tworeports1'
        first_rating = 3
        self.create_happiness_report(first_team,
                                     first_user,
                                     first_rating)

        second_team = 'anon_tworeports2'
        second_user = 'anon_tworeports2'
        second_rating = 5
        self.create_happiness_report(second_team,
                                     second_user,
                                     second_rating)

        response = self.client.get('/stats/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {first_team: first_rating,
                         second_team: second_rating}
        self.assertEqual(response.data, expected_data)

    def test_stats_anon_oneteam_tworeports(self):
        """
        Get stats endpoint with two user happiness reports on one team, anonymously
        """
        team_name = 'anon_oneteam_two'
        team = Team.objects.create(name=team_name)

        first_username = 'anon_oneteam_two1'
        first_user = self.custom_user.objects.create_user(username=first_username,
                                                          password='',
                                                          team=team)
        first_rating = 3
        Happiness.objects.create(owner=first_user,
                                 rating=first_rating)

        second_username = 'anon_oneteam_two2'
        second_user = self.custom_user.objects.create_user(username=second_username,
                                                           password='',
                                                           team=team)
        second_rating = 5
        Happiness.objects.create(owner=second_user,
                                 rating=second_rating)

        response = self.client.get('/stats/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        values = [first_rating,
                  second_rating]
        mean = statistics.mean(values)
        expected_data = {team_name: mean}
        self.assertEqual(response.data, expected_data)

def test_stats_auth_empty(self):
    """
    Get stats endpoint with no data, as user
    """
    team_name = 'stats_auth_empty'
    team = Team.objects.create(name=team_name)
    username = 'stats_auth_empty'
    user = self.custom_user.objects.create_user(username=username, password='pass', team=team)

    self.client.force_authenticate(user=user)
    response = self.client.get('/stats/')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertFalse(response.data)

def test_stats_auth_onereport(self):
    """
    Get stats endpoint with one user happiness report, as user
    """
    team_name = 'anon_onereport'
    username = 'anon_onereport'
    rating = 3
    user = self.create_happiness_report(team_name,
                                 username,
                                 rating)

    self.client.force_authenticate(user=user)
    response = self.client.get('/stats/')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    expected_levels = {rating: 1}
    expected_data = {'average': rating,
                     'levels': expected_levels}
    self.assertEqual(response.data, expected_data)

def test_stats_auth_tworeports(self):
    """
    Get stats endpoint with two user happiness reports on two teams, as user
    """
    first_team = 'anon_tworeports1'
    first_user = 'anon_tworeports1'
    first_rating = 3
    first_user = self.create_happiness_report(first_team,
                                 first_user,
                                 first_rating)

    second_team = 'anon_tworeports2'
    second_user = 'anon_tworeports2'
    second_rating = 5
    self.create_happiness_report(second_team,
                                 second_user,
                                 second_rating)

    self.client.force_authenticate(user=first_user)
    response = self.client.get('/stats/')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    expected_levels = {first_rating: 1}
    expected_data = {'average': first_rating,
                     'levels': expected_levels}
    self.assertEqual(response.data, expected_data)

def test_stats_auth_oneteam_tworeports(self):
    """
    Get stats endpoint with two user happiness reports on one team, as user
    """
    team_name = 'anon_oneteam_two'
    team = Team.objects.create(name=team_name)

    first_username = 'anon_oneteam_two1'
    first_user = self.custom_user.objects.create_user(username=first_username,
                                                      password='',
                                                      team=team)
    first_rating = 3
    Happiness.objects.create(owner=first_user,
                             rating=first_rating)

    second_username = 'anon_oneteam_two2'
    second_user = self.custom_user.objects.create_user(username=second_username,
                                                       password='',
                                                       team=team)
    second_rating = 5
    Happiness.objects.create(owner=second_user,
                             rating=second_rating)

    self.client.force_authenticate(user=first_user)
    response = self.client.get('/stats/')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    values = [first_rating,
              second_rating]
    mean = statistics.mean(values)
    expected_levels = {first_rating: 1,
                       second_rating: 1}
    expected_data = {'average': mean,
                     'levels': expected_levels}
    self.assertEqual(response.data, expected_data)
