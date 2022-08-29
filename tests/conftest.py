import datetime as dt

import pytest
import time_machine
from django.contrib import admin as django_admin
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse

from simple_analytics import admin, middleware
from simple_analytics.models import VisitPerPage

ANALYTICS_MIDDLEWARE = "simple_analytics.middleware.page_counts"
GET = "GET"
test_path = "/path"
test_username = "testuser"
test_date = dt.date(1999, 12, 31)
test_origin = "localhost"


@pytest.fixture(autouse=True)
def set_date():
    with time_machine.travel(test_date, tick=False):
        yield


@pytest.fixture
def user():
    return User.objects.create_superuser(
        username="fjm",
        email="test@mail.com",
    )


@pytest.fixture
def url():
    def _(url_name: str, **kwargs) -> str:
        return reverse(url_name, kwargs=kwargs)

    return _


@pytest.fixture
def login(client, user):
    client.force_login(user)


@pytest.fixture
def analytics_middleware(settings):
    if ANALYTICS_MIDDLEWARE not in settings.MIDDLEWARE:
        settings.MIDDLEWARE = [ANALYTICS_MIDDLEWARE, *settings.MIDDLEWARE]

    return settings


@pytest.fixture
def test_user():
    return User(username=test_username)


@pytest.fixture
def page_analytics():
    return VisitPerPage.objects.create(
        date=test_date,
        page=f"{test_path}",
        username=test_username,
        origin=test_origin,
    )


@pytest.fixture
def test_request(test_user):
    factory = RequestFactory()
    request = factory.get(test_path, HTTP_REFERER=test_origin)
    request.user = test_user

    return request


@pytest.fixture
def run_analytics(test_request):
    middleware.process_analytics(test_request, exists=True)


@pytest.fixture
def first_row_analytics():
    def _():
        return VisitPerPage.objects.first()

    return _


@pytest.fixture
def analytics_count():
    def _():
        return VisitPerPage.objects.count()

    return _


@pytest.fixture
def admin_site():
    return django_admin.AdminSite()


@pytest.fixture
def admin_instance(admin_site):
    return admin.PageAnalyticsAdmin(model=VisitPerPage, admin_site=admin_site)
