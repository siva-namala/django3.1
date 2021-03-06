from decimal import Decimal

from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save

from products.models import Product

User = settings.AUTH_USER_MODEL
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
    inventory_updated = models.BooleanField(default=False)

    def get_absolute_url(self):
        return f"orders/{self.id}/"

    def get_download_url(self):
        return f"{self.id}/download/"

    @property
    def is_downloadable(self):
        if not self.product:
            return False
        if self.product.is_digital:
            return True
        return False

    def mark_paid(self, custom_amount=None, save=False):
        paid_amount = self.total
        if custom_amount is not None:
            paid_amount = custom_amount
        self.paid = paid_amount
        self.status = 'paid'
        if not self.inventory_updated and self.product:
            self.product.remove_items_from_inventory()
            self.inventory_updated = True
        if save == True:
            self.save()
        return self.paid

    def calculate(self, save=False):
        if not self.product:
            return {}
        sub_total = self.product.price   # 29.99 -> 2999
        tax_rate = Decimal(0.12)   # 0.12 -> 12
        tax_total = sub_total * tax_rate   # 1.29 1.2900000003
        tax_total = Decimal("%.2f" % tax_total)
        total = sub_total + tax_total
        total = Decimal("%.2f" % total)
        totals = {
            "sub_total": sub_total,
            "tax": tax_total,
            "total": total
        }
        for k, v in totals.items():
            setattr(self, k, v)  # instance.sub_total = totals['sub_total']
            if save == True:
                self.save()  # obj.save()
        return totals


def order_pre_save(sender, instance, *args, **kwargs):
    instance.calculate(save=False)


pre_save.connect(order_pre_save, sender=Order)


# def order_post_save(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.calculate(save=True)


# post_save.connect(order_post_save, sender=Order)



