import uuid

from django.db import models


# Create your models here.
class ToolsModel(models.Model):
    tool_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tool_name = models.CharField(max_length=128, blank=False, null=False)
    display_name = models.CharField(max_length=128, default='')
    description = models.CharField(max_length=1024, default='')
    logo = models.CharField(max_length=1024, default='')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.tool_name

    class Meta:
        db_table = 'tools'
