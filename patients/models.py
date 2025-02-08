from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"