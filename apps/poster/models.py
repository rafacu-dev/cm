from django.db import models
from apps.shop.models import Shop
from django.conf import settings

domain = settings.DOMAIN

class Poster(models.Model):
    id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,null=False,blank=False)
    image = models.ImageField(upload_to = 'poster')
    dimension = models.FloatField()
    text = models.TextField(blank = False, null = False)
    color = models.IntegerField(blank = True, null = True)
    font= models.IntegerField(blank = True, null = True)
    date = models.DateTimeField(auto_now_add=True)

    
    def getImage(self):
        if self.image:
            if "poster" in str(self.image.url): 
                image =  "http://" + domain + self.image.url
            else:
                image =  str(self.image)
            return image
        return ''

        
class StaticPoster(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to = 'static_poster')
    is_active = models.BooleanField(default=True)
    
    def getImage(self):
        if self.image:
            return "http://" + domain + self.image.url
        return '' 