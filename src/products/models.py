from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=220)
    short_code = models.CharField(max_length=30)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
