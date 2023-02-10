"""Module test_happiness providing unit tests for the happiness model"""
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.test import TestCase
from api.models import Happiness

class HappinessUnitTests(TestCase):
    """
    Unit tests for the happiness model
    """

    def setUp(self):
        """
        Happiness objects require an owner
        """
        name = 'paolo'
        self.custom_user = get_user_model()
        self.user = self.custom_user.objects.create_user(username=name)

    def test_create_happiness_base(self):
        """
        Create a happiness report
        """
        rating = 3
        happiness = Happiness.objects.create(owner=self.user,
                                             rating=rating)
        self.assertEqual(happiness.rating, rating)
        self.assertEqual(str(happiness), str(happiness.id))

    def test_create_happiness_noowner(self):
        """
        Attempt to create a happiness report with no owner
        """
        rating = 3
        with self.assertRaises(IntegrityError):
            Happiness.objects.create(rating=rating)

    def test_create_happiness_norating(self):
        """
        Attempt to create a happiness report with no rating
        """
        with self.assertRaises(IntegrityError):
            Happiness.objects.create(owner=self.user)
