from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# from taggit.serializers import (TagListSerializerField, TaggitSerializer)


class Cake(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateField()
    description = models.TextField()
    recipe = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'cake_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for cake_id: {self.cake_id} @{self.url}"


