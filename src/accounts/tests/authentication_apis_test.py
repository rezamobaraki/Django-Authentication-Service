from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationAPITestCase(APITestCase):

    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            cellphone='09123456789', password='password123', first_name='test', last_name='user'
        )
        cls.new_user_data = {
            'cellphone': '09123456789', 'first_name': 'test', 'last_name': 'user', 'email': 'email@email.com'
        }

    def test_authentication_viewset_creates_authentication_request(self):
        url = reverse('accounts:authentication:authentication-list')
        data = {'username': 'testuser'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration_viewset_verifies_registration(self):
        url = reverse('accounts:authentication:registration-verify')
        data = {'verification_code': '123456'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration_viewset_submits_information(self):
        url = reverse('registration-information')
        data = {'username': 'testuser', 'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration_viewset_completes_registration(self):
        url = reverse('registration-complete')
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_viewset_logs_in_user(self):
        url = reverse('login-list')
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration_viewset_verification_fails_with_invalid_code(self):
        url = reverse('registration-verify')
        data = {'verification_code': 'invalid'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_viewset_information_fails_with_missing_data(self):
        url = reverse('registration-information')
        data = {'username': 'testuser'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_viewset_completion_fails_with_weak_password(self):
        url = reverse('registration-complete')
        data = {'username': 'testuser', 'password': '123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_viewset_fails_with_invalid_credentials(self):
        url = reverse('login-list')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
