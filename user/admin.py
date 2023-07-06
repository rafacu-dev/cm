from django.contrib import admin
from .models import CheckCode
from django.contrib.auth import get_user_model
User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('user','is_staff','is_superuser','is_active','last_login' )
    list_display_links = ('user', )
    search_fields = ('user','is_staff','is_superuser','is_active','last_login' )

admin.site.register(User, UserAdmin)
admin.site.register(CheckCode)