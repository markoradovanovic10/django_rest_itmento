from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Profile


class ProfileAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.profile = Profile.objects.create(user=self.user, bio='', birth_date='1993-03-03')
        self.url = reverse('profile-detail', args=[self.profile.id])

    def test_update_birth_date(self):
        data = {'birth_date': '2000-01-01'}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.profile.refresh_from_db()
        self.assertEqual(str(self.profile.birth_date), '2000-01-01')