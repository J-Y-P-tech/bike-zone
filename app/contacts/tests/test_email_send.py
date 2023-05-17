from django.core import mail
from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.core.mail import send_mail


class TestSendEmail(TestCase):
    """
    Test successful email sending using locmem EmailBackend
    """

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email(self):
        """
        Confirm that send_mail function is called with the correct data
        To mock send_email we replace EMAIL_BACKEND
        This backend stores the sent emails in memory,
        allowing us to retrieve them later for assertions.
        """

        # Create a superuser for testing
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )

        # Trigger the code that sends the email
        bike_title = 'Example Bike'
        admin_info = User.objects.filter(is_superuser=True).first()
        admin_email = admin_info.email
        send_mail(
            'New Car Inquiry',
            'You have a new inquiry for the bike ' + bike_title +
            '. Please login to your admin panel for more info.',
            'jordan.yurukov@gmail.com',
            [admin_email],
            fail_silently=False,
        )

        # Assert that the email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Assert the email content
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, 'New Car Inquiry')
        self.assertEqual(sent_email.body, 'You have a new inquiry for the bike ' + bike_title +
                         '. Please login to your admin panel for more info.')
        self.assertEqual(sent_email.from_email, 'jordan.yurukov@gmail.com')
        self.assertEqual(sent_email.to, [admin_email])
