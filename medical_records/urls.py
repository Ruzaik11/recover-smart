from django.urls import path
from .views import MedicalRecordView

urlpatterns = [
    path('api/medical_record/my_records', MedicalRecordView.getMyRecords),
    path('api/medical_record', MedicalRecordView.as_view()),
    #path('api/medical_record/edit/<int:pk>/', Patients.edit),
    path('api/medical_record/<int:pk>', MedicalRecordView.as_view()),
]
