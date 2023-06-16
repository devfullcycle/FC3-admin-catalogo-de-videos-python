

from dataclasses import dataclass
from typing import List
import pytest
import os
from colorama import Fore, Style


def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="run tests using the specified env file from /envs folder",
    )
    parser.addoption(
        "--group",
        action="store",
        default=None,
        help="run tests only from the specified group",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(
    early_config: pytest.Config,
    parser: pytest.Parser,
    args: List[str]
):
    parser_args = parser.parse_known_args(args)
    env = parser_args.env
    os.environ.setdefault('APP_ENV', env)
    print(
        f"{Fore.BLUE}\n\n**** Running tests using .env.{env} ****\n\n{Style.RESET_ALL}"
    )
    #early_config._env = env


def pytest_runtest_setup(item: pytest.Item):
    group_mark = item.get_closest_marker("group")

    group_option = item.config.getoption("--group")

    if group_option:
        if group_mark is None or group_option not in group_mark.args:
            pytest.skip("test requires group {group_option}")


@pytest.fixture(scope="function")
def enable_migration(django_db_use_migrations) -> bool:
    return EnableMigration(is_migrations_enabled=django_db_use_migrations)


MigrationCommandBackup = None


def pytest_configure(config: pytest.Config):
    from django.core.management.commands import migrate
    global MigrationCommandBackup
    MigrationCommandBackup = migrate.Command


@dataclass
class EnableMigration:

    is_migrations_enabled: bool

    def run(self):
        return EnableMigration(is_migrations_enabled=self.is_migrations_enabled)
   
    def __enter__(self):

        if self.is_migrations_enabled:
            return

        from django.core.management.commands import migrate
        from django.conf import settings

        settings.MIGRATION_MODULES = {}
        migrate.Command = MigrationCommandBackup

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_migrations_enabled:
            return

        from pytest_django.fixtures import _disable_migrations
        _disable_migrations()
