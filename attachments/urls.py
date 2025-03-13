from django.urls import path
from .views import AttachmentView

urlpatterns = [
    path('api/attachments', AttachmentView.as_view()),
    path('api/attachments/list', AttachmentView.getFile),
    path('api/attachments/file', AttachmentView.getSingleFile),
]