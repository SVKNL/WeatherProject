from django.test import TestCase
from django.urls import reverse


class ForecastViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        url = reverse('city', kwargs={'loc': "London"})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_view_forecast_list_all(self):
        url = reverse('city', kwargs={'loc': "London"})
        resp = self.client.get(url)
        self.assertTrue(len(resp.context['weather']) == 24)
        self.assertTrue(len(resp.context['shortlist']) == 6)
