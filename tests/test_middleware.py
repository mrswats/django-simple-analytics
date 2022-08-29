import pytest

from .conftest import test_date, test_origin


@pytest.mark.parametrize(
    "url_name, status_code",
    [
        ("test-url", 200),
        ("this-url-does-not-exist", 404),
    ],
)
@pytest.mark.urls("tests.urls")
@pytest.mark.django_db
def test_analytics_middleware_creates_objects(
    url, client, analytics_middleware, analytics_count, url_name, status_code
):
    response = client.get(url(url_name))
    assert response.status_code == status_code
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
    url, client, analytics_middleware, first_row_analytics, url_name, status_code, status
):
    response = client.get(url(url_name))
    assert response.status_code == status_code
    assert first_row_analytics().exists == status


@pytest.mark.urls("tests.urls")
@pytest.mark.django_db
def test_analytics_middleware_ignores_query_params(url, client, first_row_analytics):
    resp = client.get(url("test-url"), data={"param1": "AAAAAAAAAAA", "param2": "OOOOOOOOOOOO"})
    assert resp.request.get("QUERY_STRING") != ""
    assert first_row_analytics().page == "/test-url-path/"


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
    url, client, analytics_middleware, analytics_count, ignored_path
):
    client.get(url("test-ignored-url", custom_path=ignored_path))
    assert analytics_count() == 0


@pytest.mark.parametrize(
    "field, expected_value",
    [
        ("date", test_date),
        ("page", "/test-url-path/"),
        ("method", "GET"),
        ("origin", ""),
        ("username", "AnonymousUser"),
    ],
    ids=[
        "request date is recorded",
        "Path matches request path",
        "Method is defults to GET",
        "REFERER header not present defaults to empty string",
        "non-logged in users defaults to AnonymousUser",
    ],
)
@pytest.mark.django_db
@pytest.mark.urls("tests.urls")
def test_process_analytics_records_field(
    url, client, analytics_middleware, first_row_analytics, field, expected_value
):
    client.get(url("test-url"))
    assert getattr(first_row_analytics(), field) == expected_value


@pytest.mark.parametrize(
    "field, expected_value",
    [
        ("date", test_date),
        ("page", "/test-url-path/"),
        ("method", "GET"),
        ("origin", test_origin),
        ("username", "fjm"),
    ],
    ids=[
        "request date is recorded",
        "Path matches request path",
        "Method is defults to GET",
        "REFERER header not present defaults to empty string",
        "non-logged in users defaults to AnonymousUser",
    ],
)
@pytest.mark.django_db
@pytest.mark.urls("tests.urls")
def test_process_analytics_records_logged_in_users_records_fields(
    url, login, client, analytics_middleware, first_row_analytics, field, expected_value
):

    client.get(url("test-url"), HTTP_REFERER=test_origin)
    assert getattr(first_row_analytics(), field) == expected_value
