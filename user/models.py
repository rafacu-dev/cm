from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
import random

from utils.bot import sendNotificationTelegram


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        

        code_confirm = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
        #code_confirm = 11111
        sendNotificationTelegram("@MaileenBarbarita",code_confirm)
        register_code = CheckCode.objects.create(user = user, code_confirm = code_confirm)
        register_code.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        

        return user

User = settings.AUTH_USER_MODEL

class CheckCode(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    code_confirm = models.CharField(max_length=5, blank = False, null = False)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    #name = models.CharField(max_length=100, blank = False, null = False)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    

    def __str__(self):
        return self.email

class Config(models.Model):
    key = models.CharField(max_length=50, blank = False, null = False,unique=True)
    value = models.CharField(max_length=100, blank = False, null = False)