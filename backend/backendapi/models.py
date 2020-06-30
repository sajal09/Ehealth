from django.db import models

# Create your models here.

class patient_signup(models.Model):
     
     email = models.EmailField(max_length=254, unique=True)
     name = models.CharField(max_length=120, null=True)
     date = models.DateField(null=True)
     password = models.CharField(max_length=256)


class specialist_signup(models.Model):

     email = models.EmailField(max_length=254, unique=True)
     name = models.CharField(max_length=120, null=True)
     speciality = models.CharField(max_length=256, null=True)
     experience = models.IntegerField(null=True)
     place_of_practice = models.TextField(max_length=1000, null=True)
     postal_code = models.IntegerField(null=True)
     password = models.CharField(max_length=256)
