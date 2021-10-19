from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import Group
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField('First Name', blank=True, max_length=100)
    last_name = models.CharField('Last Name', blank=True, max_length=100)
    # username = models.CharField('Username', max_length=100)
    # password = models.CharField('Password', max_length=100)
    email = models.CharField('Email', unique=True, max_length=100)

#     class Meta:
#         permissions = (
#             ("can_volunteer", "Volunteer at Events"),
#             ("can_donate", "Donate at Events"),
#             ("admin_roles", "Admin Permissions")
#         )