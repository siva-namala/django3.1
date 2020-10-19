from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from emails.forms import InventoryWailistForm
from .models import Product
from .forms import ProductModelForm


def home(request):
    return render(request, "products/home.html", {})


@login_required
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
    return render(request, "products/detail_in_productsapp.html", context)


def search_view(request):
    query = request.GET.get('q')
    qs = Product.objects.filter(title__icontains=query)
    context = {"msg": "welcome to search page",
               "query": query,
               "obj_list": qs
               }
    return render(request, 'products/search.html', context)


@staff_member_required
def product_create_view(request):
    form = ProductModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user  # saves with user
        obj.image = request.FILES.get('image')
        obj.protected_media = request.FILES.get('protected_media')
        obj.save()
        form = ProductModelForm()
        # return redirect('/products')
    context = {"form": form}
    return render(request, 'form.html', context, status=201)


def featured_product(request):
    qs = Product.objects.filter(featured=True)
    product = None
    if qs.exists():
        product = qs.first()
    # add product id to session for checkout page
    if product:
        if product.can_order:   # can_order method is property
            request.session['product_id'] = product.id

    # form
    form = InventoryWailistForm(request.POST or None, product=product)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.product = product
        if request.user.is_authenticated:
            obj.user = request.user
        obj.save()
        return redirect("/waitlist-success")

    context = {
        "form": form,
        "object": product,
        "can_order": product.can_order
    }
    return render(request, 'products/detail_in_productsapp.html', context)
