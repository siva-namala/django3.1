from django.http import Http404
from django.shortcuts import render

from .models import Product


def home(request):
    return render(request, "products/home.html", {})


def product_list_view(request):
    query_set = Product.objects.all()
    context = {"object_list": query_set}
    return render(request, "products/product_list.html", context)


def product_detail_view(request, pk):
    try:
        obj = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        raise Http404
    context = {"object": obj}
    return render(request, "products/product_detail.html", context)