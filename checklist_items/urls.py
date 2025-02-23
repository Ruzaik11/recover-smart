from django.urls import path
from .views import ChecklistsItem

urlpatterns = [
    path('api/checklists/item/', ChecklistsItem.as_view()),
    #path('api/checklists/edit/<int:pk>/', Checklists.edit),
    path('api/checklists/item/<int:pk>', ChecklistsItem.as_view()),
]