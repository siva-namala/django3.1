from django.http import Http404
from django.shortcuts import render

from .models import Product
from .forms import ProductModelForm


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


def search_view(request):
    query = request.GET.get('q')
    qs = Product.objects.filter(title__icontains=query)
    context = {"msg": "welcome to search page",
               "query": query,
               "obj_list": qs
               }
    return render(request, 'products/search.html', context)


def product_create_view(request):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # obj.user = request.user
        obj.save()
        form = ProductModelForm()
        # return redirect('/products')
    context = {"form": form}
    return render(request, 'forms.html', context)
