from django.db import models

class Doctor(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    specialization = models.CharField(max_length=250)
    email = models.CharField(max_length=250)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"