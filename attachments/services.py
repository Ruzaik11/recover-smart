# services.py
import os
import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Attachment

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
            return None, None

    def deleteFile(self):
        # Add deletion logic later
        pass

    def getFiles(self):
        # Add retrieval logic later
        pass