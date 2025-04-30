from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=200)
    api_key = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)

