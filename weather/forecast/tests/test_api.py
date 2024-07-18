from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from forecast.models import City
from weather.serializers import CitySerializer
from weather.urls import urlpatterns


class RequestsApiTestCase(APITestCase):



    def test_get(self):
        request_1 = City.objects.create(name='Wow', requests=5)
        request_2 = City.objects.create(name='Lol', requests=15)
        serializer_data = CitySerializer([request_1, request_2], many=True).data
        url = reverse('city-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


