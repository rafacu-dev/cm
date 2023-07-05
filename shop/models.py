from django.db import models
from user.models import User
from django.conf import settings

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    image = models.ImageField(upload_to = 'shop')
    name = models.CharField(max_length=100, blank = False, null = False)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(default="")
    open = models.BooleanField(default = True)
    
    rating = models.FloatField(default = 0.0)
    averageTime = models.FloatField(default = 0.0)

    verified = models.BooleanField(default = False)


    def getImage(self):
        if self.image:
            return "https://" + settings.ALLOWED_HOSTS[0] + self.image.url
        return '' 