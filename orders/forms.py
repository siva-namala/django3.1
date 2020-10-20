from django import forms

from .models import Order


class OrderModelForm(forms.ModelForm):
    shipping_address = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "shipping-address-class form-control",
                "rows": 3,
                "placeholder": "Your shipping address."
            }
        )
    )
    billing_address = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "billing-address-class form-control",
                "rows": 3,
                "placeholder": "Your billing address."
            }
        )
    )

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
        shipping_addr = cleaned_data.get("shipping_address")
        # check inventory exists
        if self.product:
            if not self.product.can_order:  # can_order is property not function to call
                raise forms.ValidationError("Product is out of stock. Cannot order now.")
            if (self.product.requires_shipping and shipping_addr is None) or (self.product.requires_shipping and
                                                                              shipping_addr == ""):
                # raise forms.ValidationError("Please enter your shipping address.")
                self.add_error("shipping_address", "Please enter your shipping address.")

        return cleaned_data
