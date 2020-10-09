from django.http import Http404
from django.shortcuts import render

from .models import Product


def home(request):
    return render(request, "products/home.html", {})


def product_detail(request, pk):
    try:
        obj = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        raise Http404
    context = {"product": obj}
    return render(request, "products/detail.html", context)