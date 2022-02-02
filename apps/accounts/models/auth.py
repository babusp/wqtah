"""
models file
"""
# python imports


# django imports
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# local imports
from apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User Model Class
    """
    # user_name = models.CharField(max_length=50, unique=True)
    Admin = 1
    BusinessOwner = 2
    EndUser = 3
    StaffUser = 4
    ROLES = (
        (Admin, 'Admin'),
        (BusinessOwner, 'BusinessOwner'),
        (EndUser, 'EndUser'),
        (StaffUser, 'StaffUser')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    country_code = models.CharField(max_length=5, null=True, blank=True)
    phone_no = models.CharField(unique=True, max_length=17, null=True, blank=True)
    role = models.IntegerField(default=3, choices=ROLES)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=20, blank=True, null=True)
    verification_token_created_at = models.DateTimeField(null=True, blank=True)
    forgot_pass_token = models.CharField(max_length=20, blank=True, null=True)
    forgot_pass_token_created_at = models.DateTimeField(null=True, blank=True)

    # otp related fields
    otp = models.CharField(max_length=10,null=True)
    otp_verified = models.BooleanField(default=False)

    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)

    # here username_field is django defined field in account model, used for account identification.
    USERNAME_FIELD = 'phone_no'

    # list of the field names that will be prompted for when creating a account via the
    # createsuperuser management command.
    REQUIRED_FIELDS = ["email","first_name"]

    def save(self, *args, **kwargs):
        if not self.id and not self.email:
            self.email = self.email
        super(User, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.phone_no

    @property
    def full_name(self):
        name = ""
        name += self.first_name if self.first_name else ""
        name += " {}".format(self.last_name) if self.last_name else ""
        return name

    def get_token(self):
        """
        :return: access-token in json format
        """
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
