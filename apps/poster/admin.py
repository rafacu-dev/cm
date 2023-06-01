from django.contrib import admin

from .models import StaticPoster

class StaticPosterAdmin(admin.ModelAdmin):
    list_display = ('id','image','is_active')

admin.site.register(StaticPoster, StaticPosterAdmin)