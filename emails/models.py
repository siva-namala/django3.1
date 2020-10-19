from django.conf import settings
from django.db import models

from products.models import Product

User = settings.AUTH_USER_MODEL


class InventoryWaitlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
