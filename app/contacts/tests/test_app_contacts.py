from django.test import TestCase
from django.apps import apps


class TestContactsAppExists(TestCase):
    """
    Test that confirms that app contacts exists
    """

    def test_app_exists(self):
        app_label = 'contacts'
        app_exists = apps.is_installed(app_label)
        self.assertTrue(app_exists, f"The app '{app_label}' does not exist.")
