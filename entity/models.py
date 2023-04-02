import uuid

from django.db import models


class EntityModel(models.Model):
    entity_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.UUIDField()
    entity_type_id = models.IntegerField()
    entity_name = models.CharField(null=False, max_length=245)
    email_id = models.EmailField()
    phone_number = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    has_branch = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()
