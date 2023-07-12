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
    path("project_view/<int:id>", views.project_view, name="project_view"),
    path("update_members/<int:id>", views.update_members, name="update_members"),
    path("create_ticket/<int:project_id>", views.create_ticket, name="create_ticket"),
    path("update_ticket/<int:project_id>", views.update_ticket, name="update_ticket"),

    #api routes
    path('api/project/<int:pk>/', views.project_detail, name='project-detail'),
    path('api/delete_project/<int:id>', views.delete_project, name='delete_project'),
    path("project_view/<int:project_id>/delete_member/<int:member_id>/", views.delete_member, name="delete_member"),
    path("project_view/<int:project_id>/delete_ticket/<int:ticket_id>/", views.delete_ticket, name="delete_ticket"),
    path("project_view/<int:project_id>/edit_ticket/<int:ticket_id>/", views.edit_ticket, name="edit_ticket"),
    path("project_view/<int:project_id>/get_ticket_details/<int:ticket_id>/", views.get_ticket_details, name="get_ticket_details"),
    path("save_comment/", views.save_comment, name='save_comment'),
    path("delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment")

]  
