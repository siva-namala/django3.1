from django.db import models
from django.conf import settings

from .storages import ProtectedStorage

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    title = models.CharField(max_length=65)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    protected_media = models.FileField(upload_to='p_products/', storage=ProtectedStorage,
                                       null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    inventory = models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def has_inventory(self):
        return self.inventory > 0

    def remove_items_from_inventory(self, count=1, save=True):
        current_inv = self.inventory
        current_inv -= count
        self.inventory = current_inv
        if save:
            self.save()
        return self.inventory

