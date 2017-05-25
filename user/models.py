from django.db import models
from django.contrib.auth.models import User


class Area(models.Model):
    area_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.pk)


class Plot(models.Model):
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)
    plot_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    lng = models.CharField(max_length=100)
    alt = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    polygon = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.pk)


class Public(models.Model):
    plot_code = models.ForeignKey(Plot, on_delete=models.CASCADE)
    floor_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    lng = models.CharField(max_length=100)
    alt = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    polygon = models.CharField(max_length=1000)

    def __str__(self):
        return self.name+" "+str(self.floor_id)


class Floor(models.Model):
    plot_id = models.ForeignKey(Plot, on_delete=models.CASCADE)
    floor_id = models.CharField(max_length=1000)
    description = models.CharField(default="NULL", max_length=1000)

    def __str__(self):
        return str(self.pk)


class POI(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    floor_id = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)
    webaddress = models.CharField(default="NULL", max_length=100, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    lat = models.CharField(default="", max_length=100, blank=True)
    lng = models.CharField(default="", max_length=100, blank=True)
    alt = models.CharField(default="", max_length=100, blank=True)
    type = models.CharField(default="", max_length=100, blank=True)
    polygon = models.CharField(default="", max_length=1000, blank=True)
    assigned = models.BooleanField(default=False)

    def __str__(self):
        return self.name+" "+str(self.floor_id)


class File(models.Model):
    file = models.FileField(null=True, blank=True)

