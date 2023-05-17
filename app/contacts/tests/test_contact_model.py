from django.test import TestCase
from contacts.models import Contact
from django.urls import reverse
from django.utils import timezone
from contacts.admin import ContactAdmin
from django.contrib import admin


class TestContactModel(TestCase):
    """Tests that Contact Model is implemented correctly"""

    def setUp(self):
        """Create a record in Contact with all required data"""

        self.contact = Contact.objects.create(
            first_name='First name',
            last_name='Last name',
            bike_id=0,
            customer_need='Customer need',
            bike_title='Bike title',
            city='City',
            state='State',
            email='test@example.com',
            phone='1234567890',
            message='Test message',
            user_id=1,
            create_date=timezone.now()
        )

    def test_contact_fields(self):
        """
        Test that the created record contains specific data
        """
        self.assertEqual(self.contact.first_name, 'First name')
        self.assertEqual(self.contact.last_name, 'Last name')
        self.assertEqual(self.contact.bike_id, 0)
        self.assertEqual(self.contact.customer_need, 'Customer need')
        self.assertEqual(self.contact.bike_title, 'Bike title')
        self.assertEqual(self.contact.city, 'City')
        self.assertEqual(self.contact.state, 'State')
        self.assertEqual(self.contact.email, 'test@example.com')
        self.assertEqual(self.contact.phone, '1234567890')
        self.assertEqual(self.contact.message, 'Test message')
        self.assertEqual(self.contact.user_id, 1)
        self.assertIsNotNone(self.contact.create_date)

    def test_contact_str(self):
        """
        Test that the string representation of created object is an email
        """
        self.assertEqual(str(self.contact), 'test@example.com')

    def test_contacts_registered_admin(self):
        """
        Test that model contacts is registered in Admin
        """
        model_admin = admin.site._registry.get(Contact)
        self.assertIsNotNone(model_admin)
        self.assertIsInstance(model_admin, ContactAdmin)
