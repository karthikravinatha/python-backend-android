import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from django.core.validators import MaxLengthValidator


# Create your models here.
class UserModel(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    entity_id = models.UUIDField(default=None)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    mobile_number = models.CharField(max_length=12, null=False, blank=False)
    email_id = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_super_user = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email_id'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email_id

    class Meta:
        index_together = [['user_id'], ['first_name'], ['email_id']]
        db_table = 'users'
