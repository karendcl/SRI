from django.db import models

# Create your models here.

class Documents(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    author = models.CharField(max_length=100)
    genres = models.CharField(max_length=300)
    url = models.CharField(max_length=300)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


