from django.db import models
from django.conf import settings


# Create your models here.

class SearchQuery(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    query = models.CharField(max_length=220, null=True)
    category = models.CharField(max_length=20, null=True)
    start_date = models.DateField(null=True)

