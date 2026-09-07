from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from jobs.constants import CacheKeys
from jobs.models import Category
from users.models import UserRole

User = get_user_model()

class RedisCachingTestCase(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(
            email='cachetest@example.com',
            password='password123',
            role=UserRole.ADMIN,
        )
        self.category = Category.objects.create(name='Original Category')

    def test_category_list_caching_and_invalidation(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('category-list')
        key = CacheKeys.get_category_list_key()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(cache.get(key))

        create_data = {'name': 'New Category', 'description': 'Testing cache invalidation'}
        create_response = self.client.post(url, create_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(cache.get(key))
