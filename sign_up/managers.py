from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext


class UserManager(BaseUserManager):
    def create(self, first_name, last_name, mobile_number, email_id, is_super_user, password):
        if not email_id:
            raise ValueError(gettext("User Must Have email address"))

        user = self.model(first_name=first_name, last_name=last_name, mobile_number=mobile_number,
                          email_id=email_id, is_super_user=is_super_user)
        encrypted_password = make_password(password)
        user.password = encrypted_password
        # user.set_password(password) # this is not working
        user.save(using=self._db)
        return user
