import pytest
from django.contrib.auth.models import User
from django.urls import reverse

ANALYTICS_MIDDLEWARE = "simple_analytics.middleware.page_counts"


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
def get(client, url):
    def _(
        url_name: str,
        expected_status_code: int = 200,
        follow: bool = True,
        **url_kwargs,
    ):
        response = client.get(url(url_name, **url_kwargs), follow=follow)
        assert response.status_code == expected_status_code
        return response

    return _
