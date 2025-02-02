from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_editable = ['is_staff']
    list_per_page = 10
    list_max_show_all = 100
    ordering = ["username"]

    actions = ["make_staff", "make_not_staff"]

    def make_staff(self, request, queryset):
        queryset.update(is_staff=True)

    make_staff.short_description = "Make selected users staff"

    def make_not_staff(self, request, queryset):
        queryset.update(is_staff=False)

    make_not_staff.short_description = "Make selected users not staff"



admin.site.register(User, CustomUserAdmin)
# admin.site.register(Todo, TodoAdmin)

