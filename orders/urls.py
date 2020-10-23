from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('checkout/', views.order_check_out),
    path('success/', views.my_orders_view),
    path('orders/', views.my_orders_view),
    path('orders/<int:order_id>/download/', views.download_order),
    path('success/<int:order_id>/download/', views.download_order),
]