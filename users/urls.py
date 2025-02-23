from django.urls import path
from .views import Users

urlpatterns = [ 
    path('api/users', Users.as_view(), name='users'),
    path('api/users/edit/<int:pk>/', Users.edit),
    path('api/users/<int:pk>', Users.as_view(), name='users'),
]
