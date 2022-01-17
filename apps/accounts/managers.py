"""
managers file
"""
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    User Manager Class
    """
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        """All email providers treat emails in a case-insensitive manner."""
        email = email or ''
        return email.lower()

    def _create_user(self, email, password, is_staff,
                     is_superuser, **extra_fields):
        extra_fields.pop('username', None)
        email = self.normalize_email(email)

        if 'is_active' in extra_fields:
            is_active = extra_fields.pop('is_active')
        else:
            is_active = True

        user = self.model(email=email, is_staff=is_staff,
                          is_active=is_active, is_superuser=is_superuser,
                          **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(email__iexact=username)
