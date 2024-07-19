from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from weather.serializers import CitySerializer
from .meteo import Forecast
import datetime
from .models import City
from django.db.models import F



# Вспомогательная функция, которая принимает поисковый запрос, применяет класс Forecast из meteo.py
# также обновляет историю просмотров, далее при условии, что введен верный город, добавляет его в БД и увеличивает кол-во
# просмотров. На выходе дает словарь с переменными для подстановки в html шаблоны. Обработка класса Forecast
# сводится к переводу шорт-прогноза в словарь для подстановки в шаблон, также выдает списки с часами и датами для
# местного часового пояса начиная с текущего момента
def helper(request, city):
    if 'recently_viewed' in request.session:
        if city in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(city)
        request.session['recently_viewed'].insert(0, city)
        if len(request.session['recently_viewed']) > 10:
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [city]
    request.session.modified = True
    recently = request.session['recently_viewed']
    forecast = Forecast(city)
    if City.objects.filter(name = city).exists():
        City.objects.filter(name = city).update(requests = F('requests') + 1)
    elif city == 'url "home"':
        pass
    else:
        record = City()
        record.name = city
        record.requests = 1
        record.save()
    autocomplete = City.objects.all()
    now_time = forecast.get_date_now()
    now_hour = now_time.hour + 1
    hours_list = []
    dateList = []
    for i in range(7):
        dateList.append((now_time + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))

    if now_hour < 0:
        for i in range(now_hour, (now_hour + 23)):
            hours_list.append(i)
    else:
        for i in range(now_hour, 24):
            hours_list.append(i)
        for i in range(23 - (24 - now_hour)):
            hours_list.append(i)
    shortList = []
    for i in range(1,7):
        proxy = forecast.get_shortdaily(i)
        proxy['date'] = dateList[i]
        shortList.append(proxy)
    context = { 'city': city.capitalize(),
                'weather': forecast.get_full_list('weather'), 'hour': hours_list,
                'humidity': forecast.get_full_list('humidity'),
                'precipitation': forecast.get_full_list('precipitation'),
                'is_rain': forecast.is_sad_full(), 'datelist': dateList, 'shortlist': shortList,
                'recently': recently, 'autocomplete': autocomplete}
    return context

# главная страница и поиск
def index(request):
    if request.method == 'POST':
        city = (request.POST.get('city')).capitalize()
        # обработка криво введенного города
        try:
            context = helper(request, city)
        except:
            return render(request, 'not_found.html')
        return render(request, 'forecast.html', context)
    if 'recently_viewed' in request.session:
        recently = request.session['recently_viewed']
    else:
        recently = None
    return render(request, 'index.html', {'recently': recently})





# Для работы ссылок в истории поиска и поиска, когда уже есть инфа о погоде
def weather_search(request, loc):
    if request.method == 'POST':
        city = (request.POST.get('city')).capitalize()
        try:
            context = helper(request, city)
        except:
            return render(request, 'not_found.html')
        return render(request, 'forecast.html', context)
    else:
        city = loc
        try:
            context = helper(request, city)
        except:
            return render(request, 'not_found.html')
        return render(request, 'forecast.html', context)

# вью класс для API
class RequestsView(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer