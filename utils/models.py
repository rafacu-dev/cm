from django.db import models
from django.conf import settings

class Config(models.Model):
    key = models.CharField(max_length=50, blank = False, null = False,unique=True)
    value = models.CharField(max_length=100, blank = False, null = False)