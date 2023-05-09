from django.core.files.storage import default_storage
from bikes.management.commands.populate_data import Command
from django.db import transaction
from django.test import TestCase
from unittest.mock import patch
from bikes.models import Bike
from django.core.files import File
from PIL import Image
from io import BytesIO
import os
import tempfile


class TestPopulateBikesCommand(TestCase):

    def setUp(self):
        self.command = Command()
        # self.folder_path = 'dwnld'
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder_path = self.temp_dir.name
        self.filename = "black_image.jpg"

    def tearDown(self):
        self.command.clear_all_bikes_data()

    @patch('bikes.management.commands.populate_data.ddg.download')
    def test_populate_bikes_command(self, mock_download):
        """
        Test populate_bikes on populate_data Command
        by using mocking on ddg (import DuckDuckGoImages as ddg)
        Test that function downloads at least 1 image and uploads it
        to the volume.
        """

        def side_effect(*args, **kwargs):
            """ This functions mocks the behaviour og ddg by creating image
            1x1 pixels instead of downloading it."""
            max_urls = kwargs.get('max_urls', 0)
            image = Image.new('RGB', (1, 1), color='black')
            file_path = os.path.join(self.folder_path, self.filename)
            image.save(file_path)
            # print(f'1x1 image created {file_path} with max_urls {max_urls}')

        # Set the side_effect of mock_download to our custom function
        mock_download.side_effect = side_effect

        # Run the command
        self.command.populate_bikes()

        # Check that 15 bikes and its images are created
        self.assertEqual(Bike.objects.count(), 15)

        # Loop through each bike in the list
        for bike_data in self.command.bikes_data:
            # Check if a bike record exists in the database with the same data
            bike = Bike.objects.filter(bike_title=bike_data['bike_title'],
                                       state=bike_data['state'],
                                       city=bike_data['city'],
                                       color=bike_data['color'],
                                       model=bike_data['model'],
                                       year=bike_data['year'],
                                       condition=bike_data['condition'],
                                       price=bike_data['price'],
                                       description=bike_data['description'],
                                       body_style=bike_data['body_style'],
                                       engine=bike_data['engine'],
                                       transmission=bike_data['transmission'],
                                       miles=bike_data['miles'],
                                       vin_no=bike_data['vin_no'],
                                       milage=bike_data['milage'],
                                       fuel_type=bike_data['fuel_type'],
                                       no_of_owners=bike_data['no_of_owners'],
                                       is_featured=bike_data['is_featured']
                                       ).first()

            self.assertIsNotNone(bike, f"Expected bike record for {bike_data['bike_title']} "
                                       f"not found in the database")

            # Check if Primary photo uploaded to Bike model
            self.assertTrue(bike.bike_photo.url)

    @patch('bikes.management.commands.populate_data.ddg.download')
    def test_populate_bike_no_image_downloaded(self, mock_download):
        """ Test the behaviour of populate_bikes in case of no image downloaded by ddg """

        # ddg.download will not run and no image will be downloaded
        mock_download.return_value = True

        # Run the command
        self.command.populate_bikes()

        # Check that 15 bikes and its images are created
        self.assertEqual(Bike.objects.count(), 15)

        # Loop through each bike in the list
        for bike_data in self.command.bikes_data:
            # Check if a bike record exists in the database with the same data
            bike = Bike.objects.filter(bike_title=bike_data['bike_title'],
                                       state=bike_data['state'],
                                       city=bike_data['city'],
                                       color=bike_data['color'],
                                       model=bike_data['model'],
                                       year=bike_data['year'],
                                       condition=bike_data['condition'],
                                       price=bike_data['price'],
                                       description=bike_data['description'],
                                       body_style=bike_data['body_style'],
                                       engine=bike_data['engine'],
                                       transmission=bike_data['transmission'],
                                       miles=bike_data['miles'],
                                       vin_no=bike_data['vin_no'],
                                       milage=bike_data['milage'],
                                       fuel_type=bike_data['fuel_type'],
                                       no_of_owners=bike_data['no_of_owners'],
                                       is_featured=bike_data['is_featured']
                                       ).first()

            self.assertIsNotNone(bike, f"Expected bike record for {bike_data['bike_title']} "
                                       f"not found in the database")

            # Check if Primary photo uploaded to Bike model
            self.assertTrue(bike.bike_photo.url)

            # Load the image from the bike object
            uploaded_image = Image.open(bike.bike_photo)

            # Check that the dimensions of the image are 600x600
            self.assertEqual(uploaded_image.size, (600, 600))
