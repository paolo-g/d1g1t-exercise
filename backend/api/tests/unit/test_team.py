"""Module test_team providing unit tests for the team model"""
from django.db.utils import (
    DataError, IntegrityError
)
from django.test import TestCase
from api.models import Team

class TeamUnitTests(TestCase):
    """
    Unit tests for the team model
    """

    def test_create_team_base(self):
        """
        Create a team
        """
        name = 'engineering'
        team = Team.objects.create(name=name)
        self.assertEqual(str(team), name)
        self.assertEqual(Team.objects.filter(name=name).count(), 1)

    def test_create_team_samename(self):
        """
        Attempt to create two teams with the same name
        """
        name = 'samename'
        Team.objects.create(name=name)
        with self.assertRaises(IntegrityError):
            Team.objects.create(name=name)

    def test_create_team_longname(self):
        """
        Attempt to create a team with an invalid name
        """
        name = 'engineeringengineeringengineeringengineering'
        with self.assertRaises(DataError):
            Team.objects.create(name=name)
