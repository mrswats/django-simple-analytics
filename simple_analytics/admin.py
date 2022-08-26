from django.contrib import admin

from simple_analytics.models import VisitPerPage


@admin.register(VisitPerPage)
class PageAnalyticsAdmin(admin.ModelAdmin[VisitPerPage]):
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
