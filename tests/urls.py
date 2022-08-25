from django import urls
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound


def dummy_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    return HttpResponse(content=":)")


def four_oh_four_view(*args, **kwargs) -> HttpResponseNotFound:
    return HttpResponseNotFound("Nothing to see")


urlpatterns = [
    urls.path("test-url-path/", dummy_view, name="test-url"),
    urls.path("non-existing-url/", four_oh_four_view, name="this-url-does-not-exist"),
    urls.path("<str:custom_path>/", dummy_view, name="test-ignored-url"),
    urls.path("favicon.ico", dummy_view, name="favicon"),
]
