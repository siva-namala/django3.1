import pathlib

from mimetypes import guess_type
from wsgiref.util import FileWrapper
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect

from products.models import Product
from .models import Order
from .forms import OrderModelForm


@login_required
def order_check_out(request):
    product_id = request.session.get('product_id') or None
    if product_id is None:
        return redirect('/')
    product = None
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        # message.success()
        return redirect('/')

    # qs = Product.objects.filter(featured=True)
    # if not qs.exists():
    #     return redirect('/products/')
    # product = qs.first()

    user = request.user

    # to stop creating more order objects for same product at same session
    order_id = request.session.get('order_id')
    order_obj = None  # to stop creating already existing order
    new_creation = False

    try:
        order_obj = Order.objects.get(id=order_id)
        # if price of product updated, add new price to existing order_obj
        order_obj.product.price = product.price
        order_obj.save()
    except Order.DoesNotExist:
        order_id = None
    if order_id is None:
        new_creation = True
        order_obj = Order.objects.create(user=user, product=product)
        request.session['order_id'] = order_obj.id

    # if created order have different product than required product, we create new order
    if (order_obj is not None) and (new_creation is False):
        if order_obj.product.id != product.id:
            order_obj = Order.objects.create(user=user, product=product)
    request.session['order_id'] = order_obj.id

    # forms
    form = OrderModelForm(request.POST or None, product=product, instance=order_obj)
    if form.is_valid():
        order_obj.shipping_address = form.cleaned_data['shipping_address']
        order_obj.billing_address = form.cleaned_data['billing_address']
        order_obj.mark_paid(save=False)
        order_obj.save()
        del request.session['order_id']
        request.session['checkout_success_order_id'] = order_obj.id
        return redirect('/success')

    context = {
        "form": form,
        "object": order_obj,
        "is_digital": product.is_digital
    }

    return render(request, 'orders/checkout.html', context)


@login_required()
def my_orders_view(request):
    qs = Order.objects.filter(status='paid', user=request.user).order_by('-id')
    return render(request, 'orders/my_orders.html', {'object_list': qs})


@login_required
def download_order(request, order_id=None, *args, **kwargs):
    """Download private media if exists."""
    if order_id is None:
        return redirect('/orders')
    # qs = Product.objects.filter(protected_media__isnull=False)
    qs = Order.objects.filter(id=order_id, user=request.user, status='paid',
                              product__protected_media__isnull=False)
    if not qs.exists():
        return redirect('/orders')
    order_obj = qs.first()
    product_obj = order_obj.product
    pk = product_obj.id
    media = product_obj.protected_media
    if not media:
        # raise Http404
        return redirect('/orders')
    product_path = media.path
    path = pathlib.Path(product_path)  # os.path
    ext = path.suffix  # .csv, .png, .jpg
    fname = f"protected-product-{order_id}-{pk}{ext}"
    if not path.exists():
        raise Http404
    with open(path, 'rb') as f:
        wrapper = FileWrapper(f)
        content_type = 'application/force-download'
        guessed_ = guess_type(str(path))[0]
        if guessed_:
            content_type = guessed_
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Disposition'] = f"attachment;filename={fname}"
        response['X-SendFile'] = f"{fname}"
        return response
