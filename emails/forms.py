from django import forms

from .models import InventoryWaitlist


class InventoryWailistForm(forms.ModelForm):
    # to get product directly without having in fields
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product') or None
        super().__init__(*args, **kwargs)
        self.product = product

    class Meta:
        model = InventoryWaitlist
        fields = [
            'email'
        ]

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        # check inventory exists
        email = cleaned_data.get('email')
        qs = InventoryWaitlist.objects.filter(product=self.product,
                                              email__iexact=email)
        # submit email more than 5 times
        if qs.count() > 5:
            # raise self.add_error("email", "10-4 we have waitlist entry for this product")
            raise forms.ValidationError("We have waitlist entry for this product")  # non_field_errors

        return cleaned_data
