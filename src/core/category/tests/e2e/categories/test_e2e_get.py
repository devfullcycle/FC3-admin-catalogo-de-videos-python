#pylint: disable=unexpected-keyword-arg
from core.__seedwork.infra.testing.helpers import make_request
from core.category.domain.entities import Category
from core.category.tests.fixture.categories_api_fixture import ListCategoriesApiFixture, SearchExpectation
import pytest
from django_app import container
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.api import CategoryResource
from core.category.tests.helpers import init_category_resource_all_none
from urllib.parse import urlencode
from rest_framework.renderers import JSONRenderer

from rest_framework.test import APIClient

@pytest.mark.group('e2e')
@pytest.mark.django_db
class TestCategoriesGetE2E:

    client_http: APIClient
    category_repository: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.client_http = APIClient()
        cls.category_repository = container.repository_category_django_orm()

    @pytest.mark.parametrize('item', ListCategoriesApiFixture.arrange_incremented_with_created_at())
    def test_execute_using_empty_search_params(self, item: SearchExpectation):
        self.category_repository.bulk_insert(item.entities)
        self.assert_response(item.send_data, item.expected)

    @pytest.mark.parametrize('item', ListCategoriesApiFixture.arrange_unsorted())
    def test_execute_using_pagination_and_sort_and_filter(self, item: SearchExpectation):
        self.category_repository.bulk_insert(item.entities)
        self.assert_response(item.send_data, item.expected)

    def assert_response(self, send_data: dict, expected: SearchExpectation.Expected):
        response = self.client_http.get(
            f'/categories/?{urlencode(send_data)}', format='json'
        )

        assert response.status_code == 200
        print(response.content)
        print(JSONRenderer().render({
            'data': [self.serialize_category(category) for category in expected.entities],
            'meta': expected.meta,
        }))
        assert response.content == JSONRenderer().render({
            'data': [self.serialize_category(category) for category in expected.entities],
            'meta': expected.meta,
        })

    def serialize_category(self, category: Category):
        return CategoryResource.category_to_response(category)['data']
