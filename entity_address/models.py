import uuid

from django.db import models


class EntityAddressModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    entity_id = models.UUIDField()
    address1 = models.CharField(max_length=245, null=False)
    address2 = models.CharField(max_length=245, blank=True)
    address3 = models.CharField(max_length=245, blank=True)
    country_id = models.IntegerField()
    state_id = models.IntegerField()
    city_id = models.IntegerField()
    is_default = models.BooleanField(default=True)
    pin_code = models.CharField(max_length=10, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()
