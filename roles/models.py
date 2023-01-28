import uuid
from django.db import models


# Create your models here.

class RoleModels(models.Model):
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, blank=False, default='')
    display_name = models.CharField(max_length=128, blank=False, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "role"
