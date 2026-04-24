from django.urls import path
from users.api.v1 import RegisterApiView

urlpatterns = [
    path('v1/register/', RegisterApiView.as_view(), name='register'),
]