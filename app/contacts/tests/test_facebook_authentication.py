from django.test import TestCase, Client
from django.urls import reverse
from allauth.socialaccount.models import SocialApp, SocialAccount
from unittest.mock import patch


class FacebookAuthenticationTest(TestCase):
    """
    Test Facebook Authentication
    """

    def setUp(self):
        self.client = Client()

    @patch('allauth.socialaccount.providers.facebook.views.FacebookOAuth2Adapter.get_provider')
    def test_facebook_login(self, mock_provider):
        """
        Mock Facebook Authentication object and test to register.
        User should be redirected to third party page that contains:
        'You are about to sign in using a third party account'
        """

        # Create a mock Facebook provider
        mock_facebook_provider = mock_provider.return_value
        mock_facebook_provider.get_app.return_value = SocialApp.objects.create(provider='facebook', name='Facebook')

        # Mock the Facebook Graph API response
        mock_facebook_provider.get_graph_api_url.return_value = 'https://graph.facebook.com/v13.0/me'
        mock_facebook_provider.get_app_access_token.return_value = 'mocked_access_token'
        mock_facebook_provider.get_json.return_value = {
            'id': '123456789',
            'name': 'John Doe',
            'email': 'john.doe@example.com'
        }

        # Perform the Facebook login
        response = self.client.get(reverse('facebook_login'))

        # Check user is redirected to a page for login confirmation
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are about')
        self.assertContains(response, 'to sign in using a third-party account from')
