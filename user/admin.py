from django.contrib import admin
from .models import Plot, POI, Area, File, Floor

admin.site.register(Area)
admin.site.register(Plot)
admin.site.register(Floor)
admin.site.register(POI)
admin.site.register(File)

