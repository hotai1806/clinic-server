from unicodedata import name
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
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')
    email = models.EmailField(null=False)

    role = models.ForeignKey(Role, null=True , on_delete=models.SET_NULL)