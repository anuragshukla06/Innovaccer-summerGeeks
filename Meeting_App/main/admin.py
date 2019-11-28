from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Meeting)
admin.site.register(models.Host)
admin.site.register(models.Guest)