"""Module test_happiness providing integration tests for happiness endpoint"""
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Team
from api.serializers import HappinessSerializer

class HappinessIntegrationTest(APITestCase):
    """
    Tests to cover happiness endpoint
    """

    def setUp(self):
        """
        Use the user model django points to
        """
        self.custom_user = get_user_model()

    def test_happiness_create(self):
        """
        Create a happiness report via POST to /happiness
        """
        rating = 3

        # need to create a team, create a user on that team, then post below
        team_name = 'happiness_create'
        team = Team.objects.create(name=team_name)
        username = 'happiness_create'
        user = self.custom_user.objects.create_user(username=username,
                                                    password='pass',
                                                    team=team)

        self.client.force_authenticate(user=user)

        url = '/happiness/'
        data = {'rating': rating}
        response = self.client.post(url,
                                    data,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = HappinessSerializer(data=response.data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, {'rating': rating})

    def test_happiness_createtoomany(self):
        """
        Attempt to create two happiness reports in the same day
        """
        rating = 3

        # need to create a team, create a user on that team, then post below
        team_name = 'createtoomany'
        team = Team.objects.create(name=team_name)
        username = 'createtoomany'
        user = self.custom_user.objects.create_user(username=username,
                                                    password='pass',
                                                    team=team)

        self.client.force_authenticate(user=user)

        url = '/happiness/'
        data = {'rating': rating}
        self.client.post(url,
                         data,
                         format='json')

        # Submit a second time
        response = self.client.post(url,
                                    data,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        error = {'errors': 'Happiness report already exists for this user today.'}
        self.assertEqual(response.data, error)
