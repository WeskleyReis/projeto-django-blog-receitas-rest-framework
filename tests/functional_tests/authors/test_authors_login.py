import pytest

from django.contrib.auth.models import User
from selenium.webdriver.common.by import By

from django.urls import reverse

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfuly(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user',
            password=string_password
        )

        # User opens the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # User enters his username and password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # User submits the form
        form.submit()

        # User sees login message with his name
        self.assertIn(
            f'Your are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        # User opens the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User try send invalid data
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(' ')
        password.send_keys(' ')

        # User submits the form
        form.submit()

        # User sees error message
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_invalid_credentials(self):
        # User opens the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User tries to send data that does not match
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        # User submits the form
        form.submit()

        # User sees error message
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

