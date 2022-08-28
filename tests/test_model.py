import pytest

from .conftest import GET, test_date, test_origin, test_path, test_username


@pytest.mark.parametrize(
    "field, expected_value",
    [
        ("date", test_date),
        ("exists", True),
        ("method", GET),
        ("origin", test_origin),
        ("page", test_path),
        ("username", test_username),
        ("view_count", 1),
    ],
)
@pytest.mark.django_db
def test_page_analytics_model_fields(page_analytics, field, expected_value):
    assert getattr(page_analytics, field) == expected_value


@pytest.mark.django_db
def test_page_analytics_model_repr(page_analytics):
    assert repr(page_analytics) == f"<VisitPerPage: /path [{test_date.strftime('%Y-%m-%d')}] - 1>"
