from django.contrib import admin
from moon_tracker.models import ScanResult, ScanResultOre, MoonAnnotation


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


class MoonAnnotationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'moon',
            'alert',
            'final_scan',
        )}),
    )

    list_display = (
        'moon',
        'alert',
        'final_scan'
    )

    readonly_fields = (
        'moon',
    )

    search_fields = (
        'moon',
        'alert',
    )

    ordering = (
        'moon',
    )


admin.site.register(ScanResult, ScanResultAdmin)
admin.site.register(MoonAnnotation, MoonAnnotationAdmin)
