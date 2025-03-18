from django.contrib import admin

from .models import Project, UserProfile, WorkLog

admin.site.register(Project)
admin.site.register(UserProfile)
admin.site.register(WorkLog)
