from django.db import models

class Entity(models.Model):
    entity_name = models.CharField(max_length=100)

    def __str__(self):
        return self.entity_name
    class Meta:
        db_table = "entity"