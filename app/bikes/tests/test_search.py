from django.core.files.storage import default_storage
from bikes.management.commands.populate_data import Command
from django.db import transaction
from django.test import TestCase
from unittest.mock import patch
from bikes.models import Bike
from django.urls import reverse
from django.core.files import File
from PIL import Image
from io import BytesIO
import os
import tempfile


class TestSearch(TestCase):
    """ Tests Search functionality """

    @patch('bikes.management.commands.populate_data.ddg.download')
    def setUp(self, mock_download):
        """ SetUp method will populate the test database with test data.
        Image download will be mocked to save time and resources."""
        self.command = Command()
        # self.folder_path = 'dwnld'
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder_path = self.temp_dir.name
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

    def test_search_available(self):
        """ Tests search view and template are available """

        url = reverse('search')
        response = self.client.get(url)

        # Assert that the response status code is 200,
        # indicating a successful response
        self.assertEqual(response.status_code, 200)

    def test_search_by_year(self):
        """ Test that correct result is returned when search by year """

        # generate the search URL with reverse
        url = reverse('search') + '?year=2013&min_price=0&max_price=150000'
        response = self.client.get(url)

        # Confirm successful response
        self.assertEqual(response.status_code, 200)
        # Make sure 1 result is returned
        self.assertEqual(len(response.context['bikes']), 1)
        # Check if the correct bike is returned
        self.assertEqual(response.context['bikes'][0].year, 2013)

    def test_search_by_body_style(self):
        """ Test that correct result is returned when search by body_style """

        # generate the search URL with reverse
        url = reverse('search') + '?body_style=Retro&min_price=0&max_price=150000'
        response = self.client.get(url)

        # Confirm successful response
        self.assertEqual(response.status_code, 200)
        # Make sure 1 result is returned
        self.assertEqual(len(response.context['bikes']), 1)
        # Check if the correct bike is returned
        self.assertEqual(response.context['bikes'][0].body_style, 'Retro')

    def test_search_by_transmission(self):
        """ Test that correct result is returned when search by transmission """

        # generate the search URL with reverse
        url = reverse('search') + '?transmission=7-speed+DCT&min_price=0&max_price=150000'
        response = self.client.get(url)

        # Confirm successful response
        self.assertEqual(response.status_code, 200)
        # Make sure 1 result is returned
        self.assertEqual(len(response.context['bikes']), 1)
        # Check if the correct bike is returned
        self.assertEqual(response.context['bikes'][0].transmission, '7-speed DCT')

    def test_search_by_location(self):
        """ Test that correct result is returned when search by location """

        # generate the search URL with reverse
        url = reverse('search') + '?city=Las+Vegas&min_price=0&max_price=150000'
        response = self.client.get(url)

        # Confirm successful response
        self.assertEqual(response.status_code, 200)
        # Make sure 1 result is returned
        self.assertEqual(len(response.context['bikes']), 1)
        # Check if the correct bike is returned
        self.assertEqual(response.context['bikes'][0].city, 'Las Vegas')

    def test_search_dynamic_title(self):
        """
        Test that search page contains title Bike Zone |
        """
        # Get all the bikes ids
        url = reverse('search')
        response = self.client.get(url)

        # Confirm that search page contains Bike Zone | as title
        self.assertContains(response, 'Bike Zone |')
