from django.db import models

class Book(models.Model):
    external_id=models.CharField(unique=True)
    title = models.CharField(max_length=500)
    author=models.CharField(max_length=255, blank = True)
    year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)

    def __iter__(self):
        return f"{self.title} - {self.author}"