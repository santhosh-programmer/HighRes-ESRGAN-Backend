from distutils.command import upload
from django.db import models

# Create your models here.
class Photo(models.Model):
    low_res=models.ImageField(upload_to="low_res/")
    high_res=models.ImageField(upload_to="high_res/", null=True, blank=True)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.low_res.name