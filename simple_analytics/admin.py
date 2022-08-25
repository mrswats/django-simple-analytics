from django.contrib import admin

from simple_analytics import models


@admin.register(models.VisitPerPage)
class PageAnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        "page",
        "method",
        "date",
        "view_count",
        "username",
        "exists",
    )

    list_filter = (
        "exists",
        "date",
        "method",
        "username",
        "page",
    )
