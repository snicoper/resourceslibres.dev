from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User, UserKarma


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    """User en admin."""
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ('slug',)
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Información personal', {
            'fields': ('first_name', 'last_name', 'email', 'slug')
        }),
        ('Avatar', {
            'fields': ('avatar',)
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )


@admin.register(UserKarma)
class UserKarmaAdmin(admin.ModelAdmin):
    list_display = ('user_receiver', 'user_vote', 'positive', 'negative')
    search_fields = ('user_receiver__username', 'user_vote__username')
    raw_id_fields = ('user_receiver', 'user_vote')
    list_per_page = 20
