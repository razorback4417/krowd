from django.db import models

# Create your models here.
class Cause(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    orgSchool = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    date = models.DateField(max_length=50)
    targetAmount = models.IntegerField(max_length=10)