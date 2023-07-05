from django.db import models

from product.models import Product
from user.models import User

class ShoppingRegistered(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=False)
    detail = models.TextField(blank = True, null = True)
    color = models.TextField(blank = True, null = True)
    size = models.TextField(blank = True, null = True)
    smell = models.TextField(blank = True, null = True)
    taste = models.TextField(blank = True, null = True)
    texture = models.TextField(blank = True, null = True)
    quantity = models.FloatField()

    price = models.FloatField(blank = False, null = False)

    latitudeDelivery = models.FloatField(blank = True, null = True)
    longitudeDelivery = models.FloatField(blank = True, null = True)
    addressDelivery = models.TextField(blank = True, null = True)

    rute = models.TextField(default="",blank = True, null = True)
    key = models.TextField(blank = False, null = False)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def coin(self):
        return "CUP"