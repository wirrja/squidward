from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.HappinessState)
admin.site.register(models.SquidFullData)
admin.site.register(models.WhiteToDB)
admin.site.register(models.GrayToDb)
