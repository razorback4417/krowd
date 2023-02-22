from django.db import models

# Create your models here.
class Cause(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    orgSchool = models.CharField(max_length=50)
    problem = models.CharField(max_length=500, null=True)
    sol = models.CharField(max_length=500, null=True)
    location = models.CharField(max_length=50)
    date = models.DateField(max_length=50)
    targetAmount = models.IntegerField()
    contribNum = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id} ({self.name})'
