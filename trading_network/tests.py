from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from trading_network.models import Link, Product, Contact
from users.models import User


class LinkTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@test1234.com',
            is_active=True,
            is_staff=True
        )
        self.user.set_password('0000')
        self.user.save()
        self.access_token = str(AccessToken.for_user(self.user))

        self.credentials = f'Bearer {self.access_token}'

        self.client.credentials(HTTP_AUTHORIZATION=self.credentials)

        self.product = Product.objects.create(
            name='test',
            model='test',
            date='2024-03-04',
        )

        self.product_2 = Product.objects.create(
            name='test_1234',
            model='test_1234',
            date='2024-03-04',
        )

        self.link = Link.objects.create(
            status_link='factory',
            name='test_2',

        )
        contact_set = {
            'email': 'test@test.com',
            'country': 'Russia',
            'city': 'Moscow',
            'street': 'test',
            'num_house': '12'
        }

        Contact.objects.create(link=self.link, **contact_set)
        self.link.products.set([self.product])

        self.link_1 = Link.objects.create(
            status_link='entrepreneur',
            supplier=self.link,
            name='test_4',

        )
        contact_set_1 = {
            'email': 'test@test.com',
            'country': 'India',
            'city': 'Mumbai',
            'street': 'test',
            'num_house': '12'
        }

        Contact.objects.create(link=self.link_1, **contact_set_1)
        self.link_1.products.set([self.product])

        self.link_2 = Link.objects.create(
            status_link='entrepreneur',
            supplier=self.link_1,
            name='test_6',

        )
        contact_set_3 = {
            'email': 'test@test.com',
            'country': 'China',
            'city': 'Beijing',
            'street': 'test',
            'num_house': '12'
        }

        self.contact = Contact.objects.create(link=self.link_2, **contact_set_3)
        self.link_2.products.set([self.product])

    def test_link_create(self):
        """Тест создание Звена торговой цепи"""

        data = {
            'status_link': 'factory',
            'name': 'test_1',
            'products': [self.product.id],
            'contact': [
                {
                    'email': 'test@test.ru',
                    'country': 'Russia',
                    'city': 'Moscow',
                    'street': 'test',
                    'num_house': '12'
                }
            ]
        }

        response_data = {
            'id': 8,
            'status_link': "Завод",
            'supplier': None,
            'name': "test_1",
            'level': 0,
            'products': [
                self.product.id
            ],
            'debt': None,
            'contact': [
                {
                    'id': 8,
                    'email': 'test@test.ru',
                    'country': 'Russia',
                    'city': 'Moscow',
                    'street': 'test',
                    'num_house': '12'
                }
            ]
        }

        response = self.client.post(
            reverse('trading_network:link_create'),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Link.objects.all().exists()
        )

        self.assertEqual(
            response.json(),
            response_data
        )

        # Проверка на запрос не активного пользователя
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            reverse('trading_network:link_create'),
            data
        )

        self.assertEqual(
            response.json(),
            {'detail': 'User is inactive', 'code': 'user_inactive'}
        )

    def test_link_list(self):
        """Тест чтение списка Звена торговой цепи"""
        response = self.client.get(
            '/link/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['count'],
            3
        )

    def test_link_list_filter(self):
        response = self.client.get(
            '/link/?country=Russia'
        )

        self.assertEqual(
            response.json()['count'],
            1
        )

    def test_link(self):
        """Тест чтение экземпляра Звена торговой цепи"""

        response = self.client.get(
            reverse('trading_network:link', args=[self.link.id]))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_link_update(self):
        """Тест Обновление экземпляра Звена торговой цепи"""
        data = {
            'status_link': 'factory',
            'name': 'test_5',
            'debt': 50,
            'products': [self.product.id],
            'contact': [
                {
                    'email': 'test@test.ru',
                    'country': 'Russia',
                    'city': 'Moscow',
                    'street': 'test',
                    'num_house': '12'
                }
            ]
        }

        response = self.client.put(
            reverse('trading_network:link_update', args=[self.link.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['debt'],
            None
        )

        data = {
            'debt': 500
        }

        response = self.client.patch(
            reverse('trading_network:link_update', args=[self.link.id]),
            data=data
        )

        self.assertEqual(
            response.json()['debt'],
            None
        )

    def test_link_delete(self):
        """Тест удаление экземпляра Звена торговой цепи"""

        response = self.client.delete(
            reverse('trading_network:link_delete', args=[self.link_2.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_valid_status_link_supplier(self):
        """Тест на валидность установки поставщика и иерархической структуры"""
        data = {
            'status_link': 'factory',
            'supplier': self.link.id,
            'name': 'test_9',
            'products': [self.product.id],
            'contact': [
                {
                    'email': 'test@test.ru',
                    'country': 'Russia',
                    'city': 'Moscow',
                    'street': 'test',
                    'num_house': '12'
                }
            ]
        }

        response = self.client.post(
            reverse('trading_network:link_create'),
            data=data
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['У завода не может быть Поставщика']}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        data_2 = {
            'status_link': 'entrepreneur',
            'name': 'test_9',
            'products': [self.product.id],
            'contact': [
                {
                    'email': 'test@test.ru',
                    'country': 'Russia',
                    'city': 'Moscow',
                    'street': 'test',
                    'num_house': '12'
                }
            ]
        }

        response = self.client.post(
            reverse('trading_network:link_create'),
            data=data_2
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Без поставщика может быть только Завод']}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        data_3 = {
            'status_link': 'entrepreneur',
            'supplier': self.link_2.id,
            'name': 'test_9',
            'products': [self.product.id],
            'contact': [
                {
                    'email': 'test@test.ru',
                    'country': 'Russia',
                    'city': 'Moscow',
                    'street': 'test',
                    'num_house': '12'
                }
            ]
        }

        response = self.client.post(
            reverse('trading_network:link_create'),
            data=data_3
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Иерархическая структура не может состоять более чем из 3 уровней']}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_valid_product_supplier_relationship(self):
        """Тест на валидность отношения продукта и поставщика"""
        data = {
            'status_link': 'entrepreneur',
            'supplier': self.link.id,
            'name': 'test_10',
            'products': [self.product_2.id],
            'contact': [
                {
                    'email': 'test@test.ru',
                    'country': 'Russia',
                    'city': 'Moscow',
                    'street': 'test',
                    'num_house': '12'
                }
            ]
        }

        response = self.client.post(
            reverse('trading_network:link_create'),
            data=data
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Продукт %s не принадлежит поставщику %s' % (self.product_2.name, self.link.name)]}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_models_str(self):
        self.assertEqual(
            str(self.link),
            'Завод - test_2 (уровень - 0)'
        )

        self.assertEqual(
            str(self.product),
            'test (модель - test)'
        )

        self.assertEqual(
            str(self.contact),
            'Beijing (test@test.com)'
        )


class ProductTestCase(APITestCase):
    def setUp(self):
        self.user2 = User.objects.create(
            email='user2@test.com',
        )
        self.user2.set_password('test')
        self.user2.save()

        self.access_token = str(AccessToken.for_user(self.user2))
        self.credentials = f'Bearer {self.access_token}'
        self.client.credentials(HTTP_AUTHORIZATION=self.credentials)

        self.product = Product.objects.create(
            name='test33',
            model='test',
            date='2024-03-04',
        )

    def test_create_product(self):
        """Тест создание продуктов"""
        data = {
            "name": "fabric",
            "model": "fabric@mail.ru",
            "date": "2022-01-21"
        }
        response = self.client.post(
            '/product/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Product.objects.all().exists()
        )

        # Проверка на запрос не активного пользователя
        self.user2.is_active = False
        self.user2.save()
        response = self.client.post(
            '/product/',
            data=data
        )
        self.assertEqual(
            response.json(),
            {'detail': 'User is inactive', 'code': 'user_inactive'}
        )

    def test_get_list(self):
        """Тест чтение списка продуктов"""
        response = self.client.get(
            '/product/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['count'],
            1
        )

    def test_product(self):
        """Тест чтение экземпляра продуктов"""
        response = self.client.get(
            f'/product/{self.product.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.product.id, 'name': 'test33', 'model': 'test', 'date': '2024-03-04'}
        )

    def test_product_update(self):
        """Тест Обновление экземпляра продуктов"""
        data = {
            "name": "fabric",
            "model": "fabric",
            "date": "2022-01-21"
        }

        response = self.client.put(
            f'/product/{self.product.id}/',
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.product.id, 'name': 'fabric', 'model': 'fabric', 'date': '2022-01-21'}
        )

    def test_product_delete(self):
        """Тест удаление экземпляра продуктов"""

        response = self.client.delete(
            f'/product/{self.product.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Product.objects.filter(pk=self.product.id).exists(),
            False
        )


class LinkAdminTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create(
            email='test@test.com',
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        self.user.set_password('0000')
        self.user.save()

        self.client.force_login(self.user)

        self.product = Product.objects.create(
            name='test',
            model='test',
            date='2024-03-04',
        )

        self.link = Link.objects.create(
            status_link='factory',
            name='test_34',

        )
        contact_set = {
            'email': 'test@test.com',
            'country': 'Russia',
            'city': 'Moscow',
            'street': 'test',
            'num_house': '12'
        }

        Contact.objects.create(link=self.link, **contact_set)
        self.link.products.set([self.product])

    def test_create_link(self):

        post_data = {
            'status_link': 'factory',
            'supplier': self.link,
            'name': 'test_1',
            'products': [self.product.id],
            'contact': [
                {
                    'email': 'test@test.ru',
                    'country': 'Russia',
                    'city': 'Moscow',
                    'street': 'test',
                    'num_house': '12'
                }
            ]
        }

        url = reverse('admin:trading_network_link_add')

        response = self.client.post(url, data=post_data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Link.objects.count(), 1
        )
