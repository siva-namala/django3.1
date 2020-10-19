from django import forms

from .models import Order


class OrderModelForm(forms.ModelForm):
    # to get product directly without having in fields
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product') or None
        super().__init__(*args, **kwargs)
        self.product = product

    class Meta:
        model = Order
        fields = [
            'shipping_address', 'billing_address'
        ]

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        # check inventory exists
        if self.product:
            if not self.product.can_order:
                raise forms.ValidationError("Product is out of stock. Cannot order now.")

        return cleaned_data
