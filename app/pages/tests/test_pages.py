
from django.urls import reverse
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from pages import models
from django.core.files.uploadedfile import SimpleUploadedFile


class PublicTests(TestCase):
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
        self.assertContains(response, 'Home')

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


class PrivateTests(TestCase):
    """ Test authenticated requests """

    def setUp(self):
        """ Create record in Team with all required data, including image"""

        # Create a sample image file for testing
        self.uploaded_file = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )

        # Create a sample Team object for testing
        self.team = models.Team.objects.create(
            first_name="John",
            last_name="Doe",
            designation="Developer",
            image=self.uploaded_file,
            facebook_link="https://www.facebook.com/johndoe",
            twitter_link="https://www.twitter.com/johndoe",
            linked_in_link="https://www.linkedin.com/in/johndoe",
        )

    def tearDown(self):
        """ Delete the uploaded image file after each test """
        self.team.image.delete()

    def test_team_model_creation(self):
        """ Test adding record to Teams and check if exists in Home template"""

        # Test if the correct template is used for rendering the view
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'pages/home.html')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Developer')
        self.assertContains(response, self.team.image)
        self.assertContains(response, 'https://www.facebook.com/johndoe')
        self.assertContains(response, 'https://www.twitter.com/johndoe')
        self.assertContains(response, 'https://www.linkedin.com/in/johndoe')
