from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User


class UserModelAdmin(BaseUserAdmin):
    list_display = ("id", "email", "name", "is_admin", "subscription")
    list_filter = ("is_admin",)
    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "subscription")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "subscription",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email", "id")
    filter_horizontal = ()


admin.site.register(User, UserModelAdmin)
