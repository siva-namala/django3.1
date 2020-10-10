from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('home/', views.home),
    path('products/', views.product_list_view),
    path('products/<int:pk>/', views.product_detail_view),
    path('products/create/', views.product_create_view),
    path('search/', views.search_view)
]
