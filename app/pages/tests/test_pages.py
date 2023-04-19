
from django.urls import reverse
from django.test import SimpleTestCase


class PublicTests(SimpleTestCase):
    """ Test unauthenticated requests """

    def test_home_page(self):
        """ Test that home page loads correctly """

        # Issue a GET request to the generated URL
        response = self.client.get('/')

        # Assert that the response status code is 200,
        # indicating a successful response
        self.assertEqual(response.status_code, 200)

        # Optionally, you can also assert the content of the response
        # to check for expected HTML
        self.assertContains(response, 'Welcome to the home page')

    def test_about_page(self):
        """ Test that about page loads correctly """

        # Use reverse to generate the URL for the home page
        url = reverse('about')

        # Issue a GET request to the generated URL
        response = self.client.get(url)

        # Assert that the response status code is 200,
        # indicating a successful response
        self.assertEqual(response.status_code, 200)

    def test_services_page(self):
        """ Test that services page loads correctly """

        # Use reverse to generate the URL for the home page
        url = reverse('services')

        # Issue a GET request to the generated URL
        response = self.client.get(url)

        # Assert that the response status code is 200,
        # indicating a successful response
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        """ Test that contact page loads correctly """

        # Use reverse to generate the URL for the home page
        url = reverse('contact')

        # Issue a GET request to the generated URL
        response = self.client.get(url)

        # Assert that the response status code is 200,
        # indicating a successful response
        self.assertEqual(response.status_code, 200)
