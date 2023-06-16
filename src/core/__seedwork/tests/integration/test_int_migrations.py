

from io import StringIO

from core.pytest_plugin import EnableMigration
import pytest
from django.db import connections
from django.core.management import call_command


@pytest.mark.django_db(databases=['default', 'test_for_migrations'], transaction=True)
class TestIntMigration:

    apps = ['category']

    def test_run_migrations(self, enable_migration: EnableMigration):
        with enable_migration.run():
            connection = connections['test_for_migrations']
            if connection.vendor == 'sqlite' and 'memory' in connection.settings_dict['NAME']:
                self.delete_all_tables_of_sqlite(connection)

            output = StringIO()
            call_command('reset_db',
                         '--database=test_for_migrations',
                         '--noinput',
                         stdout=output
                         )

            output = StringIO()
            call_command(
                'migrate',
                '--database=test_for_migrations',
                stdout=output
            )

            assert 'Applying' in output.getvalue()
            for app in self.apps:
                assert app in output.getvalue()
            assert output.getvalue().count('category') == 2

    def delete_all_tables_of_sqlite(self, connection):
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys = OFF;')
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f"DROP TABLE {table[0]};")
            cursor.execute('PRAGMA foreign_keys = ON;')

    def test_if_migrations_are_not_synced_with_db(self):
        call_command(
            'makemigrations',
            '--check',
            '--dry-run'
        )
