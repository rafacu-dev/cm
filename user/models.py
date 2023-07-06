from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
import random

from utils.bot import sendNotificationTelegram


class UserAccountManager(BaseUserManager):
    def create_user(self, user, password=None, **extra_fields):
        if not user:
            raise ValueError('Users must have an user address')
        
        #user = self.normalize_email(user)
        user = self.model(user=user, **extra_fields)

        user.set_password(password)
        user.save()
        

        code_confirm = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
        #code_confirm = 11111
        sendNotificationTelegram(f"@{user}",code_confirm)
        register_code = CheckCode.objects.create(user = user, code_confirm = code_confirm)
        register_code.save()

        return user

    def create_superuser(self, user, password, **extra_fields):
        user = self.create_user(user, password, **extra_fields)

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
    user = models.CharField(max_length=200, unique=True,null=False,blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.user



"""if not UserAccount.objects.filter(user="Admin").exists():
    UserAccount.objects.create_superuser("Admin","admin")
    print("Superusuario creado")"""