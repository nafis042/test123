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


class People(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name


class File(models.Model):
    file = models.FileField(null=True, blank=True)

