from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from products.models import Product
from .models import Order
from .forms import OrderModelForm


@login_required
def order_check_out(request):
    qs = Product.objects.filter(featured=True)
    if not qs.exists():
        return redirect('/products/')
    product = qs.first()
    user = request.user

    # to stop creating more order objects for same product at same session
    order_id = request.session.get('order_id')
    order_obj = None  # to stop creating already existing order
    new_creation = False

    try:
        order_obj = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        order_id = None
    if order_id is None:
        new_creation = True
        order_obj = Order.objects.create(user=user, product=product)
        request.session['order_id'] = order_obj.id

    # if created order have different product than required product, we create again
    if (order_obj is not None) and (new_creation is False):
        if order_obj.product.id != product.id:
            order_obj = Order.objects.create(user=user, product=product)
    request.session['order_id'] = order_obj.id

    # forms
    form = OrderModelForm(request.POST or None, product=product, instance=order_obj)
    if form.is_valid():
        order_obj.shipping_address = form.cleaned_data['shipping_address']
        order_obj.billing_address = form.cleaned_data['billing_address']
        order_obj.save()

    return render(request, 'orders/forms.html', {"form": form})
