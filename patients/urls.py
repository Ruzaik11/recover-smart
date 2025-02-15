from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Patients
import django

urlpatterns = [
    path('api/patients/', Patients.as_view()),
    path('api/patients/edit/<int:pk>/', Patients.edit),
    path('api/patients/<int:pk>/', Patients.as_view()),
]
