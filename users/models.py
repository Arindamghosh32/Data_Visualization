from django.db import models
from django.utils import timezone
#python manage.py import_data C:\jsondata.json


class Users(models.Model):
    end_year = models.IntegerField(null=True, blank=True)
    intensity = models.IntegerField(default=0, null=True)
    sector = models.CharField(max_length=100, default='')
    topic = models.CharField(max_length=100, default='')
    insight = models.TextField(default='')
    url = models.URLField(default='')
    region = models.CharField(max_length=100, default='')
    start_year = models.IntegerField(null=True, blank=True)
    impact = models.IntegerField(null=True, blank=True)
    added = models.DateTimeField(blank=True, null=True)
    published = models.DateTimeField(blank=True, null=True)  # Allow null for manual input
    country = models.CharField(max_length=100, default='')
    relevance = models.IntegerField(default=0, null=True)
    pestle = models.CharField(max_length=100, default='')
    source = models.CharField(max_length=100, default='')
    title = models.TextField(default='')
    likelihood = models.IntegerField(default=0, null=True)
    
    def save(self, *args, **kwargs):
        
        if not self.start_year:
            self.start_year = timezone.now().year
        if not self.end_year:
            self.end_year = timezone.now().year
        super().save(*args, **kwargs)

class Persons(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)


