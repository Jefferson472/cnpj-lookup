from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.core.models.CustomUser import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_trusty',)
    list_filter = ('email', 'is_staff', 'is_active', 'is_trusty',)
    # Campos que aparecem na edição do usuário
    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_permissions')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    # Campos que aparecem na adição de um usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('user_permissions',)
