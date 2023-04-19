
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from pages import models
from django.core.files.storage import default_storage


class TeamModelTest(TestCase):
    """ Test Team Model """

    def setUp(self):
        # Create a sample image file for testing
        self.uploaded_file = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )

    def tearDown(self):
        """ Delete the uploaded image file after each test """
        self.image_to_delete.delete()

    def test_team_model_creation(self):
        # Create a sample Team object for testing
        team = models.Team.objects.create(
            first_name="John",
            last_name="Doe",
            designation="Developer",
            image=self.uploaded_file,
            facebook_link="https://www.facebook.com/johndoe",
            twitter_link="https://www.twitter.com/johndoe",
            linked_in_link="https://www.linkedin.com/in/johndoe",
        )

        # Check that the Team object was created successfully
        self.assertIsInstance(team, models.Team)
        self.assertIsNotNone(team.id)
        self.assertEqual(team.first_name, "John")
        self.assertEqual(team.last_name, "Doe")
        self.assertEqual(team.designation, "Developer")
        self.assertTrue(default_storage.exists(team.image.path))
        self.assertEqual(team.facebook_link,
                         "https://www.facebook.com/johndoe")
        self.assertEqual(team.twitter_link, "https://www.twitter.com/johndoe")
        self.assertEqual(team.linked_in_link,
                         "https://www.linkedin.com/in/johndoe")
        self.assertIsNotNone(team.created_date)

        self.image_to_delete = team.image
