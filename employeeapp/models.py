from django.db import models

# Create your models here.
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % (self.client.name)

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    license_plate = models.CharField(max_length=20)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        ordering = ['client__name']

    def __str__(self):
        return "%s %s %s" % (self.client.name, self.first_name, self.last_name)