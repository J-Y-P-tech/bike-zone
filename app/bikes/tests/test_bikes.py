from django.urls import reverse
from django.test import SimpleTestCase, TestCase
import datetime


class TestWithoutModels(TestCase):
    """ Test requests without comparing information from models"""

    def test_bikes_page_loads(self):
        """ Test that bikes page loads correctly """

        url = reverse('bikes')

        # Issue a GET request to the generated URL
        response = self.client.get(url)

        # Assert that the response status code is 200,
        # indicating a successful response
        self.assertEqual(response.status_code, 200)


class TestBaseTemplate(TestCase):
    """ Test the implementation of base template with it's topbar,
    navbar and footer"""

    def helper_method(self, response):
        self.assertContains(response, 'contact@bikezone.com')
        self.assertContains(response, '+359888123456')
        self.assertContains(response, datetime.datetime.now().year)
        self.assertContains(response, reverse('about'))
        self.assertContains(response, reverse('contact'))
        self.assertContains(response, reverse('services'))

    def test_bikes_contains_phone_email(self):
        """ Test that bikes page contains correct email, phone, correct year
        abd urls to: home, about, contacts, service  """

        url = reverse('bikes')
        response = self.client.get(url)
        self.helper_method(response)
