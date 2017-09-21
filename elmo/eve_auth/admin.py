from django.contrib import admin
from eve_auth.models import EveUser


class EveUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'character_id',
            'first_name',
            'last_name',
            'last_login',
            'date_joined',
        )}),
        ('Permissions', {'fields': (
            'is_staff',
            'groups',
            'user_permissions'
        )}),
    )

    list_display = (
        'character_id',
        'first_name',
        'last_name',
        'is_staff'
    )

    list_filter = (
        'is_staff',
    )

    readonly_fields = (
        'character_id',
        'first_name',
        'last_name',
        'last_login',
        'date_joined',
    )

    search_fields = (
        'first_name',
        'last_name',
    )

    ordering = (
        'first_name',
        'last_name',
    )


admin.site.register(EveUser, EveUserAdmin)
