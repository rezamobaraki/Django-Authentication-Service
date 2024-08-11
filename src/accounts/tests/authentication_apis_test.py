# src/accounts/tests/test_authentication.py

from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


class AuthenticationAPITestCase(APITestCase):

    def setUp(self):
        self.cellphone = "+989123456781"
        self.password = "strongpassword"
        self.user = User.objects.create_user(cellphone=self.cellphone, password=self.password)

    @classmethod
    def setUpTestData(cls):
        cls.new_cellphone = "+989987654321"
        cls.new_user_data = {
            "token": "valid_token",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        cls.register_completions_data = {
            "token": "valid_token",
            "password": "new_password"
        }

    @patch('accounts.serializers.authentication.generate_login_token')
    def test_authentication_request_existing_user(self, mock_generate_login_token):
        mock_generate_login_token.return_value = "mocked_token"
        url = reverse('accounts:authentication:authentication-list')

        response = self.client.post(url, {"cellphone": self.cellphone})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], "mocked_token")
        self.assertEqual(response.data['user_state'], "old")
        mock_generate_login_token.assert_called_once_with(cellphone=self.cellphone)

    @patch('accounts.serializers.authentication.send_registration_otp')
    def test_authentication_request_new_user(self, mock_send_registration_otp):
        url = reverse('accounts:authentication:authentication-list')

        response = self.client.post(url, {"cellphone": self.new_cellphone})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_state'], "new")
        mock_send_registration_otp.assert_called_once_with(cellphone=self.new_cellphone)

    @patch('accounts.serializers.authentication.verify_registration_otp')
    @patch('accounts.serializers.authentication.generate_registration_token')
    def test_registration_verification_success(self, mock_generate_registration_token, mock_verify_registration_otp):
        mock_verify_registration_otp.return_value = True
        mock_generate_registration_token.return_value = "mocked_registration_token"
        url = reverse('accounts:authentication:registration-verify')

        response = self.client.post(url, {"cellphone": self.cellphone, "code": "123456"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], "mocked_registration_token")
        mock_verify_registration_otp.assert_called_once_with(cellphone=self.cellphone, input_otp="123456")
        mock_generate_registration_token.assert_called_once_with(cellphone=self.cellphone)

    @patch('accounts.serializers.authentication.verify_registration_token')
    @patch('accounts.serializers.authentication.store_registration_information')
    def test_registration_information_success(self, mock_store_registration_information,
                                              mock_verify_registration_token):
        mock_verify_registration_token.return_value = True
        mock_store_registration_information.return_value = "mocked_registration_token"
        url = reverse('accounts:authentication:registration-information')

        response = self.client.post(url, self.new_user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], "mocked_registration_token")
        mock_verify_registration_token.assert_called_once_with(input_token="valid_token")
        mock_store_registration_information.assert_called_once_with(**self.new_user_data)

    @patch('accounts.serializers.authentication.verify_registration_token')
    @patch('accounts.serializers.authentication.complete_registration')
    def test_registration_completion_success(self, mock_complete_registration, mock_verify_registration_token):
        mock_verify_registration_token.return_value = True
        mock_complete_registration.return_value = self.user
        url = reverse('accounts:authentication:registration-complete')

        response = self.client.post(url, self.register_completions_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        mock_verify_registration_token.assert_called_once_with(input_token=self.register_completions_data['token'])
        mock_complete_registration.assert_called_once_with(
            token=self.register_completions_data['token'],
            password=self.register_completions_data['password']
        )

    @patch('accounts.serializers.authentication.verify_login_token')
    def test_login_success(self, mock_verify_login_token):
        mock_verify_login_token.return_value = True
        url = reverse('accounts:authentication:login-list')

        data = {
            "cellphone": self.cellphone,
            "token": "valid_login_token",
            "password": self.password
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        mock_verify_login_token.assert_called_once_with(cellphone=self.cellphone, input_token="valid_login_token")
