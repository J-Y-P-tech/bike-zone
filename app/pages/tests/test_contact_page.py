from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core import mail
from unittest import mock
from django.urls import reverse


class ContactTestCase(TestCase):
    """
    Test that contact page loads the correct data
    """

    def setUp(self):
        """
        SetUp method creates an instance of the Client class
        and generates the URL for the 'contact' view
        """
        self.client = Client()
        self.url = reverse('contact')
        self.admin_user = User.objects.create_superuser(username='admin',
                                                        email='admin@example.com',
                                                        password='password')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_contact_form_submission(self):
        """
        Test submitting contact form, user has been redirected,
        confirm that email has been sent
        and Message has been returned to user
        """

        form_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'subject': 'Test Subject',
            'phone': '1234567890',
            'message': 'Test message',
        }
        response = self.client.post(self.url, data=form_data)

        # Assert that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Trigger the code that sends the email
        admin_info = User.objects.filter(is_superuser=True).first()
        admin_email = admin_info.email

        # Assert that the email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Assert the email content
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, 'You have a new message from Bike Zone website regarding Test Subject')
        self.assertEqual(sent_email.body, 'Name: John Doe. Email: john.doe@example.com. Phone: 1234567890. '
                                          'Message: Test message')
        self.assertEqual(sent_email.from_email, 'jordan.yurukov@gmail.com')
        self.assertEqual(sent_email.to, [admin_email])

    def test_contact_page_elements_present(self):
        """
        Test that the contact page contains the required HTML elements:
        - Full Name input field
        - Email input field
        - Subject input field
        - Number input field
        - Write message textarea
        - Send Message button
        """

        response = self.client.get(self.url)

        elements = [
            'input type="text" name="name" class="form-control" placeholder="Full Name" required',
            'input type="email" name="email" class="form-control" placeholder="Email" required',
            'input type="text" name="subject" class="form-control" placeholder="Subject" required',
            'input type="text" name="phone" class="form-control" placeholder="Number"',
            'textarea class="form-control" name="message" placeholder="Write message"',
            'button type="submit" class="btn btn-md button-theme">Send Message</button>'
        ]

        for element in elements:
            with self.subTest(element=element):
                self.assertContains(response, element)
