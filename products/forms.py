from django import forms

from .models import Product


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'content'
        ]

    def clean_title(self):
        data = self.cleaned_data.get('title')
        if len(data) < 4:
            raise forms.ValidationError("Title should be long")
        return data
