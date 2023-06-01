from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=False,blank=False,unique=True)
    quantityCUP = models.FloatField(blank = False, null = False)
    quantityMLC = models.FloatField(blank = False, null = False)

