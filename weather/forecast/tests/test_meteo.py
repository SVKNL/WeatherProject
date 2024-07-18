from django.test import TestCase

from forecast.meteo import Forecast

from datetime import datetime


class ForecastTestCase(TestCase):
    def test_coordinates(self):
        instance = Forecast('London')
        result = sum([instance.latitude, instance.longitude])
        self.assertAlmostEqual(sum([51.5074456, -0.1277653]), result, delta=0.2)


    def test_json_timelen(self):
        instance = Forecast('London')
        result = len(instance.timeList)
        self.assertEqual(168, result)


    def test_localtime(self):
        instance = Forecast('London')
        result = instance.get_date_now().hour - 1
        self.assertEqual(datetime.now().hour, result)






