from django.contrib import admin
from moon_tracker.models import ScanResult, ScanResultOre


class ScanResultOreInline(admin.TabularInline):
    model = ScanResultOre


class ScanResultAdmin(admin.ModelAdmin):
    inlines = [
        ScanResultOreInline,
    ]

    fieldsets = (
        (None, {'fields': (
            'owner',
            'moon',
        )}),
    )

    list_display = (
        'moon',
        'owner',
    )

    readonly_fields = (
        'moon',
        'owner',
    )

    search_fields = (
        'moon',
        'owner',
    )

    ordering = (
        'moon',
    )


admin.site.register(ScanResult, ScanResultAdmin)
