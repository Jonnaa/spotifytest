from django.db import models
from django.urls import reverse

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} ({self.id})' 
    
class Merch(models.Model):
    item = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.IntegerField()
    image = models.CharField(max_length=250)
    name = models.CharField(max_length=100)

    # Create an artist_id FK
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return reverse('merch_details', kwargs={'merch_id': self.pk})