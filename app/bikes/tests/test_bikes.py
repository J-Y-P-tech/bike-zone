from django.urls import reverse
from django.test import SimpleTestCase, TestCase
from django.core.files.storage import default_storage
from bikes.management.commands.populate_data import Command
from django.db import transaction
from unittest.mock import patch
from bikes.models import Bike
from django.core.files import File
from PIL import Image
from io import BytesIO
import os
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


class TestBikesData(TestCase):
    """
    """

    @patch('bikes.management.commands.populate_data.ddg.download')
    def setUp(self, mock_download):
        """ SetUp method will populate the test database with test data.
        Image download will be mocked to save time and resources."""
        self.command = Command()
        self.folder_path = 'dwnld'
        self.filename = "black_image.jpg"

        def side_effect(*args, **kwargs):
            """ This functions mocks the behaviour og ddg by creating image
            1x1 pixels instead of downloading it."""
            max_urls = kwargs.get('max_urls', 0)
            image = Image.new('RGB', (1, 1), color='black')
            file_path = os.path.join(self.folder_path, self.filename)
            image.save(file_path)

        # Set the side_effect of mock_download to our custom function
        mock_download.side_effect = side_effect

        # Run the command
        self.command.populate_bikes()

    def tearDown(self):
        self.command.clear_all_bikes_data()

    def test_humanize_exists(self):
        """ Test that humanize library is available on template
        and the prices are formatted correctly """
        url = reverse('bikes')
        response = self.client.get(url)
        self.assertContains(response, '4,000')


