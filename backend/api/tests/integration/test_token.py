"""Module test_token providing integration tests for token endpoint"""
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

class TokenIntegrationTest(APITestCase):
    """
    Tests to cover token endpoint
    """

    def setUp(self):
        """
        Use the user model django points to
        """
        self.custom_user = get_user_model()

    def test_token_noauth(self):
        """
        Try to delete a token without authenticating
        """
        url = '/token/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_delete(self):
        """
        Create a token and then tries to delete
        """
        username = 'token_delete'
        password = 'pass'
        self.custom_user.objects.create_user(username=username,
                                                    password=password)

        # Create the token
        create_url = '/api-token-auth/'
        create_data = {'username': username,
                       'password': password}
        create_response = self.client.post(create_url,
                                           create_data,
                                           format='json')

        self.assertEqual(create_response.status_code, status.HTTP_200_OK)

        token = create_response.json()['token']

        delete_url = '/token/'
        self.client.credentials(HTTP_AUTHORIZATION = f'Token {token}')
        delete_response = self.client.delete(delete_url)

        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.filter(key=token).count(), 0)
