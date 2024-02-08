from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phoneNo = models.CharField(max_length=20)
    addressDetails = models.JSONField()
    workExperience = models.JSONField()
    qualifications = models.JSONField()
    projects = models.JSONField()
    photo = models.TextField(blank=True)

    def __str__(self):
        return self.name



