from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('register/', views.logout_view),
]
