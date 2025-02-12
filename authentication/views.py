from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer

class Authentication(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]   # ✅ Ensure it accepts JSON requests

    def get(self, request):
        user = request.user  # Get the authenticated user
        serialized_user = UserSerializer(user)  # Serialize the user object
        return Response(serialized_user.data)  # Return the full user data

