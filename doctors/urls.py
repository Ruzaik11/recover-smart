from django.urls import path
from .views import DoctorsView

urlpatterns = [
    path('api/doctor/', DoctorsView.as_view()),
    path('api/doctor/edit/<int:pk>/', DoctorsView.edit),
    path('api/doctor/<int:pk>/', DoctorsView.as_view()),
]
