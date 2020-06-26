from django.db import models

# Create your models here.
<<<<<<< HEAD
=======

class UserGroup(models.Model):

    group = models.CharField(max_length=32)

class UserInfo(models.Model):

    nid = models.AutoField(primary_key=True)
    user = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField(default=0)
>>>>>>> development
