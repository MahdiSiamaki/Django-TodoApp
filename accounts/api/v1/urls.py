from django.urls import include, path

app_name = 'api-v1'

urlpatterns = [
    path('todo/', include('todo.api.v1.urls', namespace='todo')),
]