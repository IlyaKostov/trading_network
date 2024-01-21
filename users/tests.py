from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.management import call_command

from users.models import User


class CreateSuperuserCommandTestCase(TestCase):

    def test_create_superuser(self):
        """Тестирование Создания суперпользователя через команду"""
        call_command('csu')

        user = User.objects.all()
        self.assertTrue(user.exists())


class CreateUserTestCase(APITestCase):

    def test_create_user(self):
        """Тестирование создания пользователя"""
        data = {
            'email': 'user@example.com',
            'password': '0000'
        }

        response = self.client.post(
            reverse('users:register'),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'email': 'user@example.com'}
        )

    def test_user_str(self):
        """Тестирование метода str модели User"""
        user = User.objects.create(email='user@example.com', password='0000')
        self.assertEqual(
            str(user),
            'user@example.com'
        )
