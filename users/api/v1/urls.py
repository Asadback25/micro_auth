from django.urls import path
from users.api.v1.views import (
    RegisterApiView, VerifyOtpView, LoginApiView, LogoutApiView,
    PasswordResetRequestView, PasswordResetConfirmView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]