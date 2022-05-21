from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser
from django.conf import settings

class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Role(ModelBase):
    name = models.CharField(max_length=100)


class User(AbstractUser):
    # DOCTOR = 1
    # NURSE = 2
    # SURGEN =3

    # ROLE_CHOICES = (
    #       (DOCTOR, 'Doctor'),
    #       (NURSE, 'Nurse'),
    #       (SURGEN, 'Surgen'),
    #   )

    avatar = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    # role = models.ForeignKey(Role, null=True , on_delete=models.SET_NULL)
