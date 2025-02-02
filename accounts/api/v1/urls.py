from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from accounts.api.v1 import views
from accounts.api.v1.views import CustomTokenObtainPairView

app_name = "api-v1"


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("token/login/", views.LoginView.as_view(), name="token-login"),
    path("token/logout/", views.LogoutView.as_view(), name="token-logout"),
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path("test-email/", views.SendTestEmail.as_view(), name="test-email"),
    path("verify-email/<str:token>/", views.VerifyEmail.as_view(), name="verify-email"),
    path(
        "resend-verification-email/",
        views.ResendVerificationEmail.as_view(),
        name="resend-verification-email",
    ),
]
