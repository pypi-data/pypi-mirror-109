from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class TestUser(AbstractBaseUser, PermissionsMixin):

    '''
    This model will contain all user's authentication ßinformation
    '''

    email = models.EmailField(max_length=255, blank=False, unique=True)
    mobile_number = PhoneNumberField(unique=True, blank=True, null=True)
    
    password = models.TextField(blank=False, null=False)  
    
    is_active = models.BooleanField(default=False, blank=False, null=False)
    
    # Declare to override username to email as an authentication field.
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['password', 'mobile_number']

    def __str__(self):

        return f'User Object ({self.id})'