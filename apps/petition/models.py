from django.db import models
from apps.user.models import User
from django.conf import settings

domain = settings.DOMAIN

class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    image = models.ImageField(upload_to = 'petition')
    dimension = models.FloatField()
    text = models.TextField(blank = False, null = False)
    color = models.IntegerField(blank = True, null = True)
    font = models.IntegerField(blank = True, null = True)
    date = models.DateTimeField(auto_now_add=True)

    
    def getImage(self):
        if self.image:
            if "petition" in str(self.image.url): 
                image =  "http://" + domain + self.image.url
            else:
                image =  str(self.image)
            return image
        return '' 


        
class StaticPetition(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to = 'static_petition')
    is_active = models.BooleanField(default=True)
    
    def getImage(self):
        if self.image:
            return "http://" + domain + self.image.url
        return ''