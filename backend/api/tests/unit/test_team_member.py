"""Module test_team_member providing unit tests for custom user model"""
from django.db.utils import (
    DataError, IntegrityError
)
from django.test import TestCase
from django.contrib.auth import get_user_model
from api.models import Team

class TeamMemberUnitTests(TestCase):
    """
    Unit tests for the custom user model
    """

    def setUp(self):
        """
        Use the user model django points to for all tests
        """
        self.custom_user = get_user_model()

    def test_create_superuser(self):
        """
        Create a superuser
        """
        name = 'superuser'
        superuser = self.custom_user.objects.create_superuser(username=name)

        self.assertEqual(str(superuser), name)
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(self.custom_user.objects.filter(username=name).count(), 1)

    def test_create_user_base(self):
        """
        Create a base user
        """
        name = 'paolo'
        user = self.custom_user.objects.create_user(username=name)

        self.assertEqual(str(user), name)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(self.custom_user.objects.filter(username=name).count(), 1)

    def test_create_user_team(self):
        """
        Create a team member
        """
        name = 'teammember'
        team = Team.objects.create(name='eng')
        user = self.custom_user.objects.create_user(username=name,
                                                    password='',
                                                    team=team)

        self.assertEqual(str(user), name)
        self.assertEqual(self.custom_user.objects.filter(username=name, team=team).count(), 1)

    def test_create_user_samename(self):
        """
        Attempt to create two users with the same username
        """
        name = 'samename'
        self.custom_user.objects.create_user(username=name)
        with self.assertRaises(IntegrityError):
            self.custom_user.objects.create_user(username=name)

    def test_create_user_longname(self):
        """
        Attempt to create a user with a name that's too long
        """
        name = 'paolopaolopaolopaolopaolo'
        with self.assertRaises(DataError):
            self.custom_user.objects.create_user(username=name)
