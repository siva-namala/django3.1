from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('home/', views.home),
    path('home/<int:pk>/', views.product_detail)
]
