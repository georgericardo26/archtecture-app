from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from account.forms import CustomUserChangeForm, CustomUserCreationForm
from account.models import Client, Architecture

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('first_name', 'last_name', 'username', 'email', 'is_staff',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('deleted_in', 'is_deleted',)}),
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'cpf', 'gender']
    list_filter = ('user',)


@admin.register(Architecture)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user',]
    list_filter = ('user',)