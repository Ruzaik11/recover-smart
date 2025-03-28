from django.shortcuts import render
from attachments.services import FileUploadService
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class AttachmentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser]   # ✅ Ensure it accepts JSON and file uploads

    @api_view(['GET'])
    def getFile(request):
        id = file_id = request.GET.get('id')
        entity = request.GET.get('entity')
        service = FileUploadService()  # Create instance
        files = service.getFiles(id,entity)  # Get files
        return Response(files)

    def post(self, request):
        if 'files' in request.FILES:
            files = request.FILES.getlist('files')
            service = FileUploadService()  # Create instance
            for file in files:
                service.uploadFile(file, request.data['id'], request.data['entity'])  # Upload each file
        return Response({"success": "Files uploaded successfully"}, status=status.HTTP_201_CREATED)
    
    @api_view(['GET'])
    def getSingleFile(request):
        id = file_id = request.GET.get('file_id')
        service = FileUploadService()
        file = service.getSingleFile(id)  # Get file
        return file
