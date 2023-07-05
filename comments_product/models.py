from django.db import models

from product.models import Product
from user.models import User
from shop.models import Shop


class CommentsProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=False,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    text = models.TextField(blank = False, null = False)
    response = models.TextField(blank = True, null = True)
    date = models.DateTimeField(auto_now_add=True)