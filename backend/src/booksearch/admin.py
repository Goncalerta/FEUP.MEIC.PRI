"""Admin"""
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


class CustomUserAdmin(UserAdmin):
    """
    Custom user admin where email is the unique identifiers
    for authentication instead of usernames.
    """

    list_display = ("email",)
    ordering = ("email",)
