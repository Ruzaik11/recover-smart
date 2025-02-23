from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer
from rest_framework import status
from django.contrib.auth.models import User

import pprint
from django.db.models import Q
import sys

# Create your views here.
class Users(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]   # ✅ Ensure it accepts JSON requests

    def get(self, request):
        
        if not request.user.has_perm("auth.view_user"):
            return Response({"error": "You do not have permission to view this user record"}, status=403)

        search = request.GET.get('search', '')
        users = User.objects.filter(
            Q(username__icontains=search) | Q(email__icontains=search)
        )
        serializer = UserSerializer(users, many=True, context={'include_items': False})
        return Response(serializer.data)
    
    @api_view(['GET'])
    def edit(request, pk):
        # Check permission
        if not request.user.has_perm("auth.view_user"):
            return Response({"error": "You do not have permission to view this user record"}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Fetch the user
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the user
        user_data = UserSerializer(user).data

        return Response(user_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        
        if not request.user.has_perm("auth.add_user"):
            return Response({"error": "You do not have permission to add a user record"}, status=403)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):

        if not request.user.has_perm("auth.change_user"):
            return Response({"error": "You do not have permission to change this user record"}, status=403)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):

        if not request.user.has_perm("auth.delete_user"):
            return Response({"error": "You do not have permission to delete this user record"}, status=403)

        try:
            user = User.objects.get(pk=pk)
            if(user.username == 'admin'):
                return Response({"error": "Cannot delete admin user"}, status=403)
            if(user.id == request.user.id):
                return Response({"error": "Cannot delete own user"}, status=403)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        user.delete()
        return Response(status=204)
    
 
        
