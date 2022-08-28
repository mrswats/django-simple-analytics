import pytest

from simple_analytics import middleware


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
def test_process_analytics_existing_analytics_for_page(
    page_analytics, run_analytics, first_row_analytics
):
    assert first_row_analytics().view_count == 2
