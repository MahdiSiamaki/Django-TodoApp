from celery import shared_task
from todo.models import Todo
import requests
from django.core.cache import cache

@shared_task
def clear_completed_tasks():
    Todo.objects.filter(done=True).delete()

@shared_task
def fetch_weather_data():
    api_key = 'your_openweather_api_key'
    city = 'your_city'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    weather_data = response.json()
    cache.set('weather_data', weather_data, timeout=1200)  # Cache for 20 minutes
