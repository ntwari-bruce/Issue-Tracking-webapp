from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("layout", views.layout, name="layout"),
    
] 