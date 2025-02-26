from django.urls import path
from .views import Patients

urlpatterns = [
    path('api/patients/', Patients.as_view()),
    path('api/patients/edit/<int:pk>/', Patients.edit),
    path('api/patients/<int:pk>/', Patients.as_view()),
    path('api/auth/user/patient', Patients.userPatient),
]
