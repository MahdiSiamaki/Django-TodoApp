from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from accounts.api.v1 import views

app_name = 'api-v1'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/login/', views.LoginView.as_view(), name='token-login'),
    path('token/logout/', views.LogoutView.as_view(), name='token-logout'),
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),
]
