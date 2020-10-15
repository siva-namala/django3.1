from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product

User = get_user_model()
ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('stale', 'Stale'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_address = models.TextField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)

