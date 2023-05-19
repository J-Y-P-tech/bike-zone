from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class TestDashboard(TestCase):
    """
    Test that user is redirected to Dashboard
    after successful login or registration
    """

    def test_dashboard_login(self):
        """
        Test that user is redirected to Dashboard
        after successful login
        """

        # Create User
        self.user = User.objects.create_user(username='testuser@example.com',
                                             password='testpassword')

        # follow=True is because we get redirected
        # LogIn with user credentials
        response = self.client.post(reverse('login'),
                                    {'email': self.user.username,
                                     'password': 'testpassword'})

        # Assert that the response status code is
        # 302 indicating a successful redirect
        self.assertEqual(response.status_code, 302)

        # Assert that the response redirects to the dashboard endpoint
        self.assertRedirects(response, reverse('dashboard'))

    def test_dashboard_register(self):
        """
        Test that user is redirected to Dashboard
        after successful registration
        """

        response = self.client.post(reverse('register'),
                                    {
                                        'firstname': 'Test first name',
                                        'lastname': 'Test last name',
                                        'email': 'testregistration@example.com',
                                        'password': 'testpassword',
                                        'confirm_password': 'testpassword',

                                    })

        # 302 is the status code for redirect
        self.assertEqual(response.status_code, 302)

        # Confirm that user has been redirected to home which means
        # a successful login
        self.assertRedirects(response, reverse('dashboard'))
