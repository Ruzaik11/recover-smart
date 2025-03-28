from django.urls import path
from .views import Checklists

urlpatterns = [
    path('api/checklists/', Checklists.as_view()),
    #path('api/checklists/edit/<int:pk>/', Checklists.edit),
    path('api/checklists/<int:pk>', Checklists.as_view()),
    path('api/checklists/record/<int:pk>', Checklists.getChecklistByRecordId),
]