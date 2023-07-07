from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login_view", views.login_view, name="login_view"),
    path("logout", views.logout, name="logout"),
    path("layout", views.layout, name="layout"),
    path("create_project", views.create_project, name="create_project"),
    path("update_project", views.update_project, name="update_project"),

    #api route
    path('api/project/<int:pk>/', views.project_detail, name='project-detail'),
] 