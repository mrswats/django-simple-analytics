from django.contrib import admin

from simple_analytics.models import VisitPerPage


@admin.register(VisitPerPage)
class PageAnalyticsAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (
        "page",
        "method",
        "date",
        "view_count",
        "username",
        "exists",
        "origin",
        "user_agent",
    )

    list_filter = (
        "exists",
        "date",
        "method",
        "origin",
        "username",
        "page",
    )
