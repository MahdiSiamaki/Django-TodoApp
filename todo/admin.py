from django.contrib import admin
from  .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'due_date', 'done']
    list_filter = ['user', 'done']
    search_fields = ['title', 'description']
    list_editable = ['done']
    list_per_page = 10
    list_max_show_all = 100
    date_hierarchy = 'due_date'
    ordering = ['done', 'due_date']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('User', {'fields': ['user']}),
        ('Task', {'fields': ['title', 'description', 'due_date', 'done']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]
    add_fieldsets = [
        ('User', {'fields': ['user']}),
        ('Task', {'fields': ['title', 'description', 'due_date', 'done']}),
    ]
    actions = ['mark_as_done', 'mark_as_undone']

    def mark_as_done(self, request, queryset):
        queryset.update(done=True)

    def mark_as_undone(self, request, queryset):
        queryset.update(done=False)

    mark_as_done.short_description = 'Mark selected todos as done'
    mark_as_undone.short_description = 'Mark selected todos as undone'