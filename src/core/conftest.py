import pytest


@pytest.fixture(scope="session")
def django_db_keepdb(request) -> bool:
    from django.conf import settings
    return request.config.getvalue("reuse_db") or settings.TEST_KEEP_DB

@pytest.fixture(scope="session")
def django_db_use_migrations(request) -> bool:
    from django.conf import settings
    return request.config.getvalue("nomigrations") or settings.TEST_USE_MIGRATIONS