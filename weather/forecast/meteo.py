import requests
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder


# Класс, который по названию города находит его координаты, затем получает через АПИ json объект с данными о температуре
# и другим показателям по часам, преобразует их в списки

class Forecast():

    def __init__(self, city):
        self.city = city
        loc = Nominatim(user_agent="GetLoc")
        getLoc = loc.geocode(city)
        self.latitude = getLoc.latitude
        self.longitude = getLoc.longitude
        linkWeather = f"https://api.open-meteo.com/v1/forecast?latitude={getLoc.latitude}&longitude={getLoc.longitude}&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,rain,showers,snowfall,wind_speed_10m,wind_direction_10m&timezone=auto"
        json_forecast = requests.get(linkWeather).json()
        self.timeList = json_forecast['hourly']['time']
        self.weatherList = json_forecast['hourly']['temperature_2m']
        self.humidityList = json_forecast['hourly']['relative_humidity_2m']
        self.precipitationList = json_forecast['hourly']['precipitation_probability']
        #self.rainList = json_forecast['hourly']['rain']
        #self.snowList = json_forecast['hourly']['snowfall']
        #self.windSpeedList = json_forecast['hourly']['wind_speed_10m']
        #self.windDirList = json_forecast['hourly']['wind_direction_10m']


# метод класса, который выдает часовую зону указанного города и возвращает текущее время в ней
    def get_date_now(self):
        obj = TimezoneFinder()
        timezone = obj.timezone_at(lng=self.longitude, lat=self.latitude)
        IST = pytz.timezone(timezone)
        return datetime.now(IST)

# метод класса, который по параметру отклонения вперед от текущего дня возвращает словарь словарей для 4 фаз дня по
    # разным метрикам погоды, слабое место- хардкодинг чисел для определения фазы дня
    def get_shortdaily(self, time_delta):
        lowerBound = time_delta * 24
        upperBound = (time_delta + 1) * (24)

        shortInfo = { 'morning':{
                                'weather': round(sum(self.weatherList[(lowerBound+6):(upperBound-12)])/6, 1),
                                'humidity':round(sum(self.humidityList[(lowerBound+6):(upperBound-12)])/6, 0),
                                'precipitation': max(self.precipitationList[(lowerBound+6):(upperBound-12)])},
                                #'rain': round(sum(self.rainList[(lowerBound+6):(upperBound-12)]), 1),
                                #'snow': round(sum(self.snowList[(lowerBound+6):(upperBound-12)]), 1),
                                #'windSpeed': [min(self.windSpeedList[(lowerBound+6):(upperBound-12)]),
                                #              max(self.windSpeedList[(lowerBound+6):(upperBound-12)])],
                                #'windDir': round(sum(self.windDirList[(lowerBound+6):(upperBound-12)])/6, 0)},
                      'day': {
                                'weather': round(sum(self.weatherList[(lowerBound+12):(upperBound-6)])/6, 1),
                                'humidity':round(sum(self.humidityList[(lowerBound+12):(upperBound-6)])/6, 0),
                                'precipitation': max(self.precipitationList[(lowerBound+12):(upperBound-6)])},
                                #'rain': round(sum(self.rainList[(lowerBound+12):(upperBound-6)]), 1),
                                #'snow': round(sum(self.snowList[(lowerBound+12):(upperBound-6)]), 1),
                                #'windSpeed': [min(self.windSpeedList[(lowerBound+12):(upperBound-6)]),
                                #              max(self.windSpeedList[(lowerBound+12):(upperBound-6)])],
                                #'windDir': round(sum(self.windDirList[(lowerBound+12):(upperBound-6)])/6, 0)},
                      'evening': {
                                'weather': round(sum(self.weatherList[(lowerBound+18):(upperBound)])/6, 1),
                                'humidity':round(sum(self.humidityList[(lowerBound+18):(upperBound)])/6, 0),
                                'precipitation': max(self.precipitationList[(lowerBound+18):(upperBound)]),},
                                #'rain': round(sum(self.rainList[(lowerBound+18):(upperBound)]), 1),
                                #'snow': round(sum(self.snowList[(lowerBound+18):(upperBound)]), 1),
                                #'windSpeed': [min(self.windSpeedList[(lowerBound+18):(upperBound)]),
                                #              max(self.windSpeedList[(lowerBound+18):(upperBound)])],
                                #'windDir': round(sum(self.windDirList[(lowerBound+18):(upperBound)])/6, 0)},
                      'night': {
                                'weather': round(sum(self.weatherList[(lowerBound):(upperBound-18)])/6, 1),
                                'humidity':round(sum(self.humidityList[(lowerBound):(upperBound-18)])/6, 0),
                                'precipitation': max(self.precipitationList[(lowerBound):(upperBound-18)])}
                                #'rain': round(sum(self.rainList[(lowerBound):(upperBound-18)]), 1),
                                #'snow': round(sum(self.snowList[(lowerBound):(upperBound-18)]), 1),
                                #'windSpeed': [min(self.windSpeedList[(lowerBound):(upperBound-18)]),
                                             # max(self.windSpeedList[(lowerBound):(upperBound-18)])],
                                #'windDir': round(sum(self.windDirList[(lowerBound):(upperBound-18)])/6, 0)},

        }

        return shortInfo



# Метод класса, который принимает отклонение вперед от текущей даты и возвращает словарь по метрикам погоды со значениями
    # списками этих метрик по часам начиная с 00:00 на заданный день
    def get_daily(self, time_delta):
        lowerBound = time_delta * 24
        upperBound = (time_delta + 1) * (24)
        full_info = {
                                'weather': self.weatherList[(lowerBound):(upperBound)],
                                'humidity':self.humidityList[(lowerBound):(upperBound)],
                                'precipitation': self.precipitationList[(lowerBound):(upperBound)],}
                                #'rain': self.rainList[(lowerBound):(upperBound)],
                                #'snow': self.snowList[(lowerBound):(upperBound)],
                                #'windSpeed': self.windSpeedList[(lowerBound):(upperBound)],
                                #'windDir':self.windDirList[(lowerBound):(upperBound)]}
        return full_info

    # обработка предыдущего метода, чтобы получить тот же результат, но начиная с текущего момента и обработка перехода в
    # новый день, то есть смены времени с 23:00 на 00:00
    def get_full_list(self, type):
        now_time = self.get_date_now()
        now_hour = now_time.hour + 1
        hours_list = []
        fullList = []
        if now_hour < 0:
            fullList.append(self.get_daily(0)[type][now_hour - 1])
            for i in range(now_hour, (now_hour + 23)):
                hours_list.append(i)
                fullList.append(self.get_daily(0)[type][i])
        else:
            fullList.append(self.get_daily(0)[type][now_hour - 1])
            for i in range(now_hour, 24):
                hours_list.append(i)
                fullList.append(self.get_daily(0)[type][i])
            for i in range(23 - (24 - now_hour)):
                hours_list.append(i)
                fullList.append(self.get_daily(1)[type][i])

        return fullList


# подготовка метода для короткой инфы по дням, чтобы иметь возможность возвращать списки по типу метрики, отклонению от
    # текущей даты и фазы дня ( период тут)
    def get_short_list(self, type, time_delta, period):
        shortList = []
        shortList.append(self.get_shortdaily(time_delta)[period][type])
        return shortList

#  проверка будут ли осадки, если нет, то далее такой графы на сайте не будет, если осадки есть, то выдаст графу с их вероятностью
    def is_sad_full(self):
        if sum(self.get_full_list('precipitation')) > 0:
            return True
        else:
            return False








