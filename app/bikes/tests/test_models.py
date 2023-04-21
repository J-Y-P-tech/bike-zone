from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from bikes.models import Bike
from django.urls import reverse

class TestBikeModel(TestCase):
    """Tests that Bike Model is implemented correctly"""

    def setUp(self):
        """Create a record in Bike with all required data, including image"""

        # Create a sample image file for testing
        self.uploaded_file = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )

        self.bike = Bike.objects.create(
            bike_title='Test Bike',
            state='CA',
            city='Los Angeles',
            color='Black',
            model='Test Model',
            year=2022,
            condition='New',
            price=10000,
            description='Test description',
            bike_photo=self.uploaded_file,
            miles=0,
            vin_no='123456789',
            milage=0,
            fuel_type='Gas',
            no_of_owners='1',
            body_style='Standard',
            engine='ICE',
            transmission='Chain',
            is_featured=True
        )

    def tearDown(self):
        """Delete the uploaded image file after each test"""
        self.bike.bike_photo.delete()

    def test_bike_model_fields(self):
        """Tests that all fields are correctly implemented """

        bike = Bike.objects.get(id=self.bike.id)

        self.assertEqual(bike.bike_title, 'Test Bike')
        self.assertEqual(bike.state, 'CA')
        self.assertEqual(bike.city, 'Los Angeles')
        self.assertEqual(bike.color, 'Black')
        self.assertEqual(bike.model, 'Test Model')
        self.assertEqual(bike.year, 2022)
        self.assertEqual(bike.condition, 'New')
        self.assertEqual(bike.price, 10000)
        self.assertEqual(bike.description, 'Test description')
        self.assertEqual(bike.miles, 0)
        self.assertEqual(bike.vin_no, '123456789')
        self.assertEqual(bike.milage, 0)
        self.assertEqual(bike.fuel_type, 'Gas')
        self.assertEqual(bike.no_of_owners, '1')
        self.assertEqual(bike.is_featured, True)
        self.assertEqual(bike.body_style, 'Standard')
        self.assertEqual(bike.engine, 'ICE')
        self.assertEqual(bike.transmission, 'Chain')

    def test_image_uploaded(self):
        """ This function confirms that the test image is uploaded correctly and is visible
        in the template """

        url = reverse('bikes')
        response = self.client.get(url)
        self.assertContains(response, self.bike.bike_photo.url)
