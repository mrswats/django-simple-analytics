import re
from datetime import datetime as dt
from typing import Callable

from django.db.models import F
from django.http import HttpRequest, HttpResponse

from simple_analytics import models

EXCLUDED_PATHS = [
    "static",
    "favicon.ico",
]

STATUS_CODE_NOT_FOUND = 404


def normalize_request_path(request_path: str) -> str:
    if request_path.endswith("/") and len(request_path) != 1:
        request_path = request_path[:-1]

    return request_path


def process_analytics(
    request_path: str,
    request_method: str,
    request_user: str,
    exists: bool,
) -> None:
    analytics, created = models.VisitPerPage.objects.get_or_create(
        date=dt.today(),
        page=normalize_request_path(request_path),
        username=request_user,
        method=request_method,
        exists=exists,
    )

    if not created:
        analytics.view_count = F("view_count") + 1
        analytics.save()


def _match_path(request_path: str) -> bool:
    return any(
        re.match(rf"/?{excluded_path}/?", request_path)
        for excluded_path in EXCLUDED_PATHS
    )


def page_counts(get_response: Callable) -> Callable:
    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)

        if not _match_path(request.path):
            process_analytics(
                request.get_full_path_info(),
                request.method,
                request.user,
                exists=response.status_code != STATUS_CODE_NOT_FOUND,
            )

        return response

    return middleware
