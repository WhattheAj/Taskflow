from django.contrib import admin
from jobs.models import Category, Job, JobActivityLog, JobComment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'category', 'creator', 'assignee', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'category', 'created_at')
    search_fields = ('title', 'description', 'creator__email', 'assignee__email')
    raw_id_fields = ('creator', 'assignee')

@admin.register(JobComment)
class JobCommentAdmin(admin.ModelAdmin):
    list_display = ('job', 'author', 'created_at')
    search_fields = ('content', 'author__email', 'job__title')

@admin.register(JobActivityLog)
class JobActivityLogAdmin(admin.ModelAdmin):
    list_display = ('job', 'actor', 'action', 'old_status', 'new_status', 'created_at')
    list_filter = ('action', 'old_status', 'new_status', 'created_at')
    search_fields = ('action', 'job__title', 'actor__email')
