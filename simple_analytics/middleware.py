import datetime as dt
import re
from typing import Any, Callable
from urllib.parse import urlparse, urlunparse

from django.db.models import F
from django.http import HttpRequest, HttpResponse

from simple_analytics.models import VisitPerPage

EXCLUDED_PATHS = [
    "static",
    "favicon.ico",
]

STATUS_CODE_NOT_FOUND = 404

CallableMiddleware = Callable[[HttpRequest], HttpResponse]


def normalize_request_path(request_path: str) -> str:
    if request_path.endswith("/") and len(request_path) != 1:
        request_path = request_path[:-1]

    return request_path


def remove_query_params_from_url(url: str) -> str:
    schema, netloc, path, *_ = urlparse(url)
    return urlunparse((schema, netloc, path, "", "", ""))


def process_analytics(request: HttpRequest, **kwargs: Any) -> VisitPerPage:
    referer_url = request.META.get("HTTP_REFERER", "")
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    analytics, created = VisitPerPage.objects.update_or_create(
        date=dt.date.today(),
        page=request.path,
        method=request.method or "",
        username=str(request.user),
        origin=remove_query_params_from_url(referer_url),
        user_agent=user_agent,
        **kwargs,
    )

    if not created:
        analytics.view_count = F("view_count") + 1
        analytics.save()

    return analytics


def _match_path(request_path: str) -> bool:
    return any(re.match(rf"/?{excluded_path}/?", request_path) for excluded_path in EXCLUDED_PATHS)


def page_counts(get_response: CallableMiddleware) -> CallableMiddleware:
    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)

        if not _match_path(request.path):
            process_analytics(request, exists=response.status_code != STATUS_CODE_NOT_FOUND)

        return response

    return middleware
