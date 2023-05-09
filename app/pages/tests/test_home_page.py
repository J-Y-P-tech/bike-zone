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


class TestHomePage(TestCase):
    """
    Test that Home page performs as expected.
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

    def test_search_home_page(self):
        """ Tests that search on home page given the correct information
        from the select menus based on the data it is populated with """

        # Issue a GET request to the generated URL
        response = self.client.get('/')

        # Get bikes_data from commands > populate_data
        bikes_data = self.command.bikes_data
        for bike in bikes_data:
            self.assertContains(response, '<option value="' + str(bike['model']) + '">'
                                + str(bike['model']) + '</option>')
            self.assertContains(response, '<option value="' + str(bike['city']) + '">'
                                + str(bike['city']) + '</option>')
            self.assertContains(response, '<option value="' + str(bike['year']) + '">'
                                + str(bike['year']) + '</option>')
            self.assertContains(response, '<option value="' + str(bike['body_style']) + '">'
                                + str(bike['body_style']) + '</option>')
