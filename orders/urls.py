from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('checkout/', views.order_check_out),
    path('download/', views.download_order),
]
