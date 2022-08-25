import pytest
import time_machine
from django.contrib import admin as django_admin
from django.utils import timezone

from simple_analytics import admin, middleware, models

from .conftest import ANALYTICS_MIDDLEWARE

test_path = "/path"
test_user = "testuser"
test_date = timezone.now()


@pytest.fixture
def analytics_middleware(settings):
    if ANALYTICS_MIDDLEWARE not in settings.MIDDLEWARE:
        settings.MIDDLEWARE = [ANALYTICS_MIDDLEWARE, *settings.MIDDLEWARE]

    return settings


@pytest.fixture
def page_analytics():
    return models.VisitPerPage.objects.create(
        date=test_date,
        page=f"{test_path}",
        username=test_user,
    )


@pytest.fixture
def run_analytics():
    middleware.process_analytics(test_path, "GET", test_user, True)


@pytest.fixture
def first_row_analytics():
    def _():
        return models.VisitPerPage.objects.first()

    return _


@pytest.fixture
def analytics_count():
    def _():
        return models.VisitPerPage.objects.count()

    return _


@pytest.fixture
def admin_site():
    return django_admin.AdminSite()


@pytest.fixture
def admin_instance(admin_site):
    return admin.PageAnalyticsAdmin(model=models.VisitPerPage, admin_site=admin_site)


@pytest.mark.parametrize(
    "field",
    [
        "page",
        "date",
        "view_count",
        "username",
        "method",
        "exists",
    ],
)
@pytest.mark.django_db
def test_page_analytics_model_fields(page_analytics, field):
    assert hasattr(page_analytics, field)


@pytest.mark.django_db
def test_page_analytics_model_repr(page_analytics):
    assert repr(page_analytics) == f"<VisitPerPage: /path [{test_date.strftime('%Y-%m-%d')}] - 1>"


@pytest.mark.parametrize(
    "test_path",
    [
        "/some-path",
        "/some-path/",
    ],
)
def test_normalize_request_path(test_path):
    assert not middleware.normalize_request_path(test_path).endswith("/")


def test_normalize_request_path_allows_root():
    assert middleware.normalize_request_path("/") == "/"


@pytest.mark.django_db
def test_process_analytics_no_existing_analytics_for_page(run_analytics, analytics_count):
    assert analytics_count() == 1


@pytest.mark.django_db
@time_machine.travel(test_date)
def test_process_analytics_existing_analytics_for_page(
    page_analytics, run_analytics, first_row_analytics
):
    assert first_row_analytics().view_count == 2


@pytest.mark.parametrize(
    "url_name, status",
    [
        ("test-url", 200),
        ("this-url-does-not-exist", 404),
    ],
)
@pytest.mark.urls("tests.urls")
@pytest.mark.django_db
def test_analytics_middleware_creates_objects(
    get, analytics_middleware, analytics_count, url_name, status
):
    get(url_name, expected_status_code=status)
    assert analytics_count() == 1


@pytest.mark.parametrize(
    "url_name, status_code, status",
    [
        ("test-url", 200, True),
        ("this-url-does-not-exist", 404, False),
    ],
)
@pytest.mark.urls("tests.urls")
@pytest.mark.django_db
def test_analytics_middleware_creates_objects_with_status_not_found(
    get, analytics_middleware, first_row_analytics, url_name, status_code, status
):
    get(url_name, expected_status_code=status_code)
    assert first_row_analytics().exists == status


@pytest.mark.parametrize(
    "ignored_path",
    [
        "static",
        "favicon.ico",
    ],
)
@pytest.mark.django_db
@pytest.mark.urls("tests.urls")
def test_process_analytics_ignores_certain_paths(
    get, analytics_middleware, analytics_count, ignored_path
):
    get("test-ignored-url", custom_path=ignored_path)
    assert analytics_count() == 0


@pytest.mark.django_db
@pytest.mark.urls("tests.urls")
def test_process_analytics_records_anonymous_user_for_non_logged_in_users(
    get, analytics_middleware, first_row_analytics
):
    get("test-url")
    assert first_row_analytics().username == "AnonymousUser"


@pytest.mark.django_db
@pytest.mark.urls("tests.urls")
def test_process_analytics_records_logged_in_users(
    login, get, analytics_middleware, first_row_analytics
):
    get("test-url")
    assert first_row_analytics().username == "fjm"


def test_analytics_admin_list_display(admin_instance):
    admin_instance.list_display == ("page", "method", "date", "view_count", "username", "exists")


def test_analytics_admin_list_filter(admin_instance):
    admin_instance.list_filter == ("exists", "date", "method", "username", "page")
