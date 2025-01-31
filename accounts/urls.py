from django.urls import path, include
from .views import UserLoginView, UserLogoutView, UserSignupView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/v1/', include('accounts.api.v1.urls', namespace='api-v1')),
]
