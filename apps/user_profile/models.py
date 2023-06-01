from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank = False, null = False, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'user')
    latitude = models.FloatField(blank = True,null = True)
    longitude = models.FloatField(blank = True,null = True)
    address = models.TextField(default="")
    phone = models.CharField(max_length=255, default='')
    email = models.EmailField(default='')
    web = models.URLField(default='')
    whatsapp = models.CharField(max_length=20, default='')
    telegram = models.CharField(max_length=20, default='')

    def getImage(self):
        if self.image:   
            #return self.image.url
            image_url = "https://" + settings.ALLOWED_HOSTS[0] + self.image.url
            print("*******************************************************************", image_url)
            return str(image_url)
        return '' 
        
    def getUserId(self):
        return self.user.id  

    def __str__(self):
        return self.user.email
