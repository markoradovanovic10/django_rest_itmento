from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Item

class ItemAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.list_url = '/api/items/'

    def test_create_item(self):
        """
        Creates an item using the API and POST
        """
        data = {
            'name': 'Test Item',
            'description': 'This is a test item',
            'price': "10.00"
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.name, 'Test Item')
        self.assertEqual(new_item.description, 'This is a test item')
        self.assertEqual(str(new_item.price), "10.00")

    def test_update_item(self):
        """
        Updates an item using the API and PATCH
        """

        item = Item.objects.create(
            name='Test Item',
            description='This is a test item',
            price="10.00"
        )

        new_data = {
            "name" : "New Item"
        }

        response = self.client.patch(f'/api/items/{item.id}/', new_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item.refresh_from_db()

        self.assertEqual(item.name, "New Item")


