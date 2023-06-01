from django.contrib import admin

from .models import StaticPetition

class StaticPetitionAdmin(admin.ModelAdmin):
    list_display = ('id','image','is_active')

admin.site.register(StaticPetition, StaticPetitionAdmin)
