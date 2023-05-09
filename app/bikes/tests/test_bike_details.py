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


class TestPageDetails(TestCase):
    """ Tests page bike details """

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

    def test_bike_details_available(self):
        """ Tests to confirm that page bike_details exists """

        # Get all the bikes ids
        bike_ids = list(Bike.objects.values_list('id', flat=True))

        for id in bike_ids:
            url = reverse('bike_detail', args=[id])
            response = self.client.get(url)

            # Assert that the response status code is 200, indicating a successful response
            self.assertEqual(response.status_code, 200)

    def test_data_correct_bike_details(self):
        """ Loops through every record in the Bike model and confirm
        that the data is correct"""

        # Get bikes_data from commands > populate_data
        bikes_data = self.command.bikes_data
        for bike in bikes_data:
            # Read every bike from list
            for key, value in bike.items():
                # Get data from Model by bike_title
                bike_from_model = Bike.objects.filter(bike_title=bike['bike_title'])
                if key == 'bike_title':
                    continue
                self.assertEqual(str(getattr(bike_from_model.first(), key)), str(value))
