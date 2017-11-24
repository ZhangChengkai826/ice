# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class APPUser(models.Model):
    username = models.CharField(max_length=63)
    password = models.CharField(max_length=31)
    fName = models.CharField(max_length=63)
    lName = models.CharField(max_length=63)
    gender = models.CharField(max_length=7)
    birthdayY = models.IntegerField()
    birthdayM = models.IntegerField()
    birthdayD = models.IntegerField()
    hobbies = models.CharField(max_length=255)

    def __str__(self):
        return self.username