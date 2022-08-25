import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_for_missing_migrations():
    """If no migrations are detected as needed, `result`
    will be `None`. In all other cases, the call will fail,
    alerting your team that someone is trying to make a
    change that requires a migration and that migration is
    absent.
    """

    result = call_command("makemigrations", check=True, dry_run=True)
    assert not result
