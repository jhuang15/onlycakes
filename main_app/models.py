from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Cake(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateField()
    description = models.TextField(max_length=600)
    recipe = models.TextField(max_length=600)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'cake_id': self.id})