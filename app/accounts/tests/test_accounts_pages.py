from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class TestAccountPages(TestCase):
    """
    Test that pages open with code 200
    """

    def test_logout_page(self):
        """ Test that login page loads correctly """

        url = reverse('logout')

        # Issue a GET request to the generated URL
        response = self.client.get(url)

        # Assert that the response status code is
        # 302 indicating a successful redirect
        self.assertEqual(response.status_code, 302)

    def test_dashboard_page(self):
        """ Test that login page loads correctly """

        url = reverse('dashboard')

        # Issue a GET request to the generated URL
        response = self.client.get(url)

        # Assert that the response status code is 302
        # indicating a user is redirected to login page
        # because he/she has not logged in
        self.assertEqual(response.status_code, 302)


class TestLogin(TestCase):
    """
    Test that login page works as expected
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser@example.com',
                                             password='testpassword')

    def test_login_page(self):
        """ Test that login page loads correctly """

        url = reverse('login')

        # Issue a GET request to the generated URL
        response = self.client.get(url)

        # Assert that the response status code is 200 indicating a successful response
        self.assertEqual(response.status_code, 200)

    def test_login_successful(self):
        """ Test that user logged in successfully and
        is redirected to home page """

        response = self.client.post(reverse('login'),
                                    {'email': self.user.username,
                                     'password': 'testpassword'})

        # 302 is the status code for redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_unsuccessful(self):
        """ Test user with wrong credentials to be redirected to login page
        """
        response = self.client.post(reverse('login'),
                                    {'email': self.user.username,
                                     'password': 'wrongpassword'})

        # 302 is the status code for redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_email_normalized(self):
        """ Test that email has been normalized upon login """

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            # Create email with normalized email
            self.user = User.objects.create_user(username=expected,
                                                 password='testpassword')

            # Try login with email that has not been normalized
            response = self.client.post(reverse('login'),
                                        {'email': email,
                                         'password': 'testpassword'})

            # 302 is the status code for redirect
            self.assertEqual(response.status_code, 302)
            # Confirm that user has been redirected to home which means
            # a successful login
            self.assertRedirects(response, reverse('dashboard'))

    def test_message_successful_login(self):
        """ Test if html returns 'You are now logged in.'
        after successful log in """

        # follow=True is because we get redirected
        response = self.client.post(reverse('login'),
                                    {'email': self.user.username,
                                     'password': 'testpassword'},
                                    follow=True)

        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You are now logged in.')

    def test_message_invalid_credentials(self):
        """ Test if html returns 'Invalid login credentials'
                after unsuccessful log in """

        # follow=True is because we get redirected
        response = self.client.post(reverse('login'),
                                    {'email': self.user.username,
                                     'password': 'wrongpassword'},
                                    follow=True)

        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid login credentials')


class TestRegister(TestCase):
    """
    Test register page
    """

    def test_register_page(self):
        """ Test that login page loads correctly """

        url = reverse('register')

        # Issue a GET request to the generated URL
        response = self.client.get(url)

        # Assert that the response status code is 200 indicating a successful response
        self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        """
        Test successful user registration
        """

        response = self.client.post(reverse('register'),
                                    {
                                        'firstname': 'Test first name',
                                        'lastname': 'Test last name',
                                        'email': 'testregistration@example.com',
                                        'password': 'testpassword',
                                        'confirm_password': 'testpassword',

                                    })

        # 302 is the status code for redirect
        self.assertEqual(response.status_code, 302)

        # Confirm that user has been redirected to home which means
        # a successful login
        self.assertRedirects(response, reverse('dashboard'))

        # Confirm that user exists
        user_exists = User.objects.filter(username='testregistration@example.com').exists()
        self.assertTrue(user_exists)

    def test_registration_existing_email(self):
        """
        Test registration of a user that already exists.
        Should be redirected back to register.
        """
        self.client.post(reverse('register'),
                         {
                             'firstname': 'Test first name',
                             'lastname': 'Test last name',
                             'email': 'testregistration@example.com',
                             'password': 'testpassword',
                             'confirm_password': 'testpassword',

                         }, follow=True)

        response = self.client.post(reverse('register'),
                                    {
                                        'firstname': 'Test first name',
                                        'lastname': 'Test last name',
                                        'email': 'testregistration@example.com',
                                        'password': 'testpassword',
                                        'confirm_password': 'testpassword',

                                    }, follow=True)

        # 200 status code when using follow=True
        self.assertEqual(response.status_code, 200)

        # Confirm that user has been redirected to register which means
        # a login was not successful
        self.assertRedirects(response, reverse('register'))

        # Should have only 1 registered user with this email
        number_users = User.objects.filter(username='testregistration@example.com').count()
        self.assertEqual(number_users, 1)

        # Message - Email already exists
        messages = list(response.context.get('messages'))

        # We get 2 messages: 1 for registering the first user
        # and 1 for the second attempt for registration
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Email already exists!')

    def test_password_confirm_missmatch(self):
        """
        Test missmatch between password and password confirm.
        Should redirect to register and user must not be created.
        """
        response = self.client.post(reverse('register'),
                                    {
                                        'firstname': 'Test first name',
                                        'lastname': 'Test last name',
                                        'email': 'testregistration@example.com',
                                        'password': 'testpassword',
                                        'confirm_password': 'missmatchpassword',

                                    }, follow=True)

        # 200 is the status code when using follow= True
        self.assertEqual(response.status_code, 200)

        # Confirm that user has been redirected to home which means
        # a successful login
        self.assertRedirects(response, reverse('register'))

        # Confirm that user does not exist
        user_exists = User.objects.filter(username='testregistration@example.com').exists()
        self.assertFalse(user_exists)

        # Message - Password do not match
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Password do not match')

    def test_message_success_after_registration(self):
        """
        Test that message 'You are now logged in.' appears
        after successful registration
        """
        response = self.client.post(reverse('register'),
                                    {
                                        'firstname': 'Test first name',
                                        'lastname': 'Test last name',
                                        'email': 'testregistration@example.com',
                                        'password': 'testpassword',
                                        'confirm_password': 'testpassword',

                                    }, follow=True)

        # 200 status code when using follow=True
        self.assertEqual(response.status_code, 200)

        # Confirm that user has been redirected to register which means
        # a login was not successful
        self.assertRedirects(response, reverse('dashboard'))

        # Should have only 1 registered user with this email
        number_users = User.objects.filter(username='testregistration@example.com').count()
        self.assertEqual(number_users, 1)

        # Message - Email already exists
        messages = list(response.context.get('messages'))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You are now logged in.')


class TestTopBar(TestCase):
    """ Test Top bar Login, Register and Logout
    If a user is not logged in LOGIN and REGISTER should be available,
    If user is logged in Home and Logout should be available """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser@example.com',
                                             password='testpassword')

    def test_user_not_logged_in(self):
        """ Test that If a user is not logged in
        LOGIN and REGISTER are available """

        response = self.client.get('/')
        self.assertContains(response,
                            '<a href="/accounts/login" class="sign-in">'
                            '<i class="fa fa-sign-in"></i> Login</a>',
                            html=True)
        self.assertContains(response,
                            '<a href="/accounts/register" class="sign-in">'
                            '<i class="fa fa-user"></i> Register</a>',
                            html=True)

    def test_user_logged_in(self):
        """ Test if user is logged in HOME and LOGOUT are available """

        # follow=True is because we get redirected
        response = self.client.post(reverse('login'),
                                    {'email': self.user.username,
                                     'password': 'testpassword'},
                                    follow=True)
        self.assertContains(response,
                            '<a href="/" class="sign-in"><i class="fa fa-tachometer"></i> Home</a>',
                            html=True)
        self.assertContains(response, '<form action="/accounts/logout" id="logout" method="POST">')
