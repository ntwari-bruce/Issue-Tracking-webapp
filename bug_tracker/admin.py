from django.contrib import admin
from .models import CustomUser
from .models import CustomUser, Project, Ticket, Comment, Notification



class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'project_description', 'get_total_tickets', 'get_active_tickets')

    def get_total_tickets(self, obj):
        return obj.project_tickets.count()
    get_total_tickets.short_description = 'Total Tickets'

    def get_active_tickets(self, obj):
        return obj.project_tickets.filter(status='In Progress').count()
    get_active_tickets.short_description = 'Active Tickets'


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'author', 'status', 'priority')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('project', 'author')
        return queryset


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'get_total_assigned_tickets')

    def get_total_assigned_tickets(self, obj):
        return obj.assigned_tickets.count()
    get_total_assigned_tickets.short_description = 'Total Assigned Tickets'


admin.site.register(Project, ProjectAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Comment)
admin.site.register(Notification)


