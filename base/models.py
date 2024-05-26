from django.db import models

# Create your models here.
class Url(models.Model):
    link = models.URLField("URL", unique=True)
    short_url = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.link} -> {self.short_url}'
