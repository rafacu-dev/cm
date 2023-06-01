from django.db import models
from apps.petition.models import Petition
from apps.product.models import Product

class Proposal(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=False,blank=False)
    petition = models.ForeignKey(Petition,on_delete=models.CASCADE,null=False,blank=False)
    date = models.DateTimeField(auto_now_add=True)