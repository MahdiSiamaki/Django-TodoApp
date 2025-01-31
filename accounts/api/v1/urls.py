from django.urls import include, path

from accounts.api.v1 import views

app_name = 'api-v1'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
]