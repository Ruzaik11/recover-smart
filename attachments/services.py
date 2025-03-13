# services.py
import os
import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Attachment
from django.http import FileResponse, HttpResponse
from django.utils.encoding import smart_str
import mimetypes


class FileUploadService:
    def __init__(self):
        self.storage = FileSystemStorage()
        self.upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')

    def uploadFile(self, file, record_id, entity):
        try:
            # Generate unique filename
            file_path = 'uploads' + '/' + entity

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            original_filename = file.name
            file_extension = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"

            # Save the file first
            saved_filename = self.storage.save(
                os.path.join(file_path, unique_filename),
                file
            )

            # Get the file URL and path
            file_url = self.storage.url(saved_filename)
            file_path = os.path.join(settings.MEDIA_ROOT, saved_filename)

            # Create DB record AFTER successful file save
            attachment = Attachment.objects.create(
                entity=entity,
                record_id=record_id,
                url=file_url
            )

            return file_path, file_url

        except Exception as e:
            print(f"Error uploading file: {str(e)}")  # Replace with logging in production
            return None

    def getSingleFile(self, file_id):
        try:
            file = Attachment.objects.get(id=file_id)
            file_path = os.path.join(settings.MEDIA_ROOT, file.url.lstrip(settings.MEDIA_URL))
            
            if os.path.exists(file_path):
                # Determine the content type based on the file extension
                content_type, encoding = mimetypes.guess_type(file_path)
                
                # For images and most files, use FileResponse
                if content_type:
                    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
                    
                    # Set the Content-Disposition header to make the browser handle the file appropriately
                    filename = os.path.basename(file.url)
                    response['Content-Disposition'] = f'inline; filename="{filename}"'
                    
                    # To force download instead of display, use:
                    # response['Content-Disposition'] = f'attachment; filename="{filename}"'
                    
                    return response
                else:
                    # Fallback for unknown content types
                    with open(file_path, 'rb') as f:
                        response = HttpResponse(f.read())
                        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file.url)}"'
                        return response
            
            return HttpResponse("File not found", status=404)
        
        except Attachment.DoesNotExist:
            return HttpResponse("File not found", status=404)

    def getFiles(self, record_id, entity):
        try:
            files = Attachment.objects.filter(record_id=record_id, entity=entity)
            return [{
                "id": file.id,
                "entity": file.entity,
                "record_id": file.record_id,
                "url": file.url
            } for file in files]
        except Attachment.DoesNotExist:
            return None