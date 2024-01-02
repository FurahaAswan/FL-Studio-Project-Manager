from django.contrib import admin
from django.core.management import call_command
from projects.models import Project

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    actions = ['load_projects']

    def load_projects(self, request, queryset):
        folder_path = '/flps'  # Update with your default folder path
        for user in queryset:
            # Assuming 'username' is a field in your User model
            folder_path = user.username  # You can customize this based on your User model
            call_command('load_projects', folder_path)

admin.site.register(Project, ProjectAdmin)


