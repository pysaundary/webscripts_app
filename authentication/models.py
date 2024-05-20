from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from utilities.models import ControlUtility
from django.utils import timezone
from datetime import datetime,timedelta
from django.conf import settings
import jwt
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, is_active=None, email=None, username=None, first_name=None, last_name=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and
        password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('Please Provide password ')
        email = CustomUserManager.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            first_name=first_name,
            last_name=last_name,
            date_joined=now,
            **extra_fields
            )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, is_active=True, email=None, username=None, password=None, first_name=None, last_name=None, provider="usingemail"):
        """
        For Create Superuser
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(
            username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user

class Users(AbstractUser,ControlUtility):
    """
    User model as per requirements 
    """
    username = models.CharField("username", max_length=250 ,unique=True)
    email = models.EmailField("user email", max_length=254 ,unique=True,db_index=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phoneNumber = models.CharField("phone Number ", max_length=20)
    Address1 = models.CharField("Address line 1",max_length=100, null=True, blank=True)
    Address2 = models.CharField("Address line 2",max_length=100, null=True, blank=True)
    city = models.CharField("City", max_length=50, null=True, blank=True)
    pinCode = models.IntegerField("Area Pin Code", null=True, blank=True)
    
    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        tokenValue = {
            "id": self.id,
            'exp': int(dt.timestamp()),
            'username': self.username,
        }
        token = jwt.encode(tokenValue, settings.SECRET_KEY, algorithm='HS256')
        return token

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def __str__(self) -> str:
        return f"{self.email}"