from django.contrib import admin
from . import models

admin.site.register(models.Channel)
admin.site.site_header = 'E for English'
admin.site.site_title = 'E for English'
