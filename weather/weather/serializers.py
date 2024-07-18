from rest_framework.serializers import ModelSerializer

from forecast.models import City


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'requests']