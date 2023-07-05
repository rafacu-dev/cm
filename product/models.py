from django.db import models
from shop.models import Shop
from django.conf import settings
from user.models import User




class Product(models.Model):
    id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,null=False,blank=False)
    image1 = models.ImageField(upload_to = 'product')
    image2 = models.ImageField(upload_to = 'product',blank = True, null = True)
    image3 = models.ImageField(upload_to = 'product',blank = True, null = True)
    image4 = models.ImageField(upload_to = 'product',blank = True, null = True)
    image5 = models.ImageField(upload_to = 'product',blank = True, null = True)
    dimension = models.FloatField()
    
    name = models.TextField(blank = False, null = False)
    description = models.TextField(blank = True, null = True)

    price = models.FloatField()    
    delivery = models.FloatField(blank = True, null = True)

    stock = models.FloatField()
    unit = models.IntegerField()
    category = models.IntegerField()   #["Food","Technology","Gift","Toys","Medications","Utensil","Furniture","Clothing","Art","Cosmetics","Pets"]
    colors = models.TextField(blank = True, null = True)
    sizes = models.TextField(blank = True, null = True)
    tastes = models.TextField(blank = True, null = True)
    smells = models.TextField(blank = True, null = True)
    textures = models.TextField(blank = True, null = True)
    date = models.DateTimeField(auto_now_add=True)
    sales = models.IntegerField(default=0)

    
    def getImages(self):
        images = []
        domain = "https://" + settings.ALLOWED_HOSTS[0]
        if self.image1:
            images.append(domain + self.image1.url)

        if self.image2:
            images.append(domain + self.image2.url)

        if self.image3:
            images.append(domain + self.image3.url)

        if self.image4:
            images.append(domain + self.image4.url)

        if self.image5:
            images.append(domain + self.image5.url)
        return images


