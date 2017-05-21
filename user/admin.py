from django.contrib import admin
from .models import People, Plot, Public, Area, File


admin.site.register(People)
admin.site.register(Public)
admin.site.register(Area)
admin.site.register(Plot)
admin.site.register(File)
