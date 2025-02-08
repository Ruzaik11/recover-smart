from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Authentication
from django.http import HttpResponse
import django

urlpatterns = [
    path('', lambda request: HttpResponse('Django: '+django.get_version())),
    path('api/auth/user/', Authentication.as_view()),
    path('api/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
]
