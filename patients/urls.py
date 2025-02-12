from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Patients
import django

urlpatterns = [
    path('api/patients/', Patients.as_view()),
]
