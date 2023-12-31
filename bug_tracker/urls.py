from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns=[
    
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login_view", views.login_view, name="login_view"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
    path("reset_password/<str:uidb64>/<str:token>/", views.reset_password, name="reset_password"),
    path("update_password/<int:id>", views.update_password, name="update_password"),
    path("logout", views.logout, name="logout"),
    path("layout", views.layout, name="layout"),
    path("create_project", views.create_project, name="create_project"),
    path("update_project", views.update_project, name="update_project"),
    path("project_view/<int:id>", views.project_view, name="project_view"),
    path("update_members/<int:id>", views.update_members, name="update_members"),
    path("create_ticket/<int:project_id>", views.create_ticket, name="create_ticket"),
    path("update_ticket/<int:project_id>", views.update_ticket, name="update_ticket"),
    path("tickets", views.tickets, name="tickets"),
    path("notifications", views.notifications, name="notifications"),

    #api routes
    path('api/project/<int:pk>/', views.project_detail, name='project-detail'),
    path('api/delete_project/<int:id>', views.delete_project, name='delete_project'),
    path("project_view/<int:project_id>/delete_member/<int:member_id>/", views.delete_member, name="delete_member"),
    path("project_view/<int:project_id>/delete_ticket/<int:ticket_id>/", views.delete_ticket, name="delete_ticket"),
    path("project_view/<int:project_id>/edit_ticket/<int:ticket_id>/", views.edit_ticket, name="edit_ticket"),
    path("project_view/<int:project_id>/get_ticket_details/<int:ticket_id>/", views.get_ticket_details, name="get_ticket_details"),
    path("save_comment/", views.save_comment, name='save_comment'),
    path("delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("chart_data/", views.chart_data, name="chart_data"),
    path("chart_data2/", views.chart_data2, name="chart_data2"),
    path("chart_data3/", views.chart_data3, name="chart_data3"),
    path("delete_all_notifications/", views.delete_all_notifications, name="delete_all_notifications")

]  
