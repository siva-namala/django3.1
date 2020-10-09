from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=65)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
