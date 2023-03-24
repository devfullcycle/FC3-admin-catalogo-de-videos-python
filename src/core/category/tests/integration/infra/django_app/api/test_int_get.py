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


@pytest.mark.django_db
class TestCategoryResourceGetMethodInt:

    resource: CategoryResource
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = container.repository_category_django_orm()
        cls.resource = CategoryResource(**{
            **init_category_resource_all_none(),
            'list_use_case': container.use_case_category_list_categories
        })

    @pytest.mark.parametrize('item', ListCategoriesApiFixture.arrange_incremented_with_created_at())
    def test_execute_using_empty_search_params(self, item: SearchExpectation):
        self.repo.bulk_insert(item.entities)
        self.assert_response(item.send_data, item.expected)

    @pytest.mark.parametrize('item', ListCategoriesApiFixture.arrange_unsorted())
    def test_execute_using_pagination_and_sort_and_filter(self, item: SearchExpectation):
        self.repo.bulk_insert(item.entities)
        self.assert_response(item.send_data, item.expected)

    def assert_response(self, send_data: dict, expected: SearchExpectation.Expected):
        request = make_request(
            http_method='get',
            url=f'/?{urlencode(send_data)}'
        )
        response = self.resource.get(request)

        assert response.status_code == 200
        assert response.data == {
            'data': [self.serialize_category(category) for category in expected.entities],
            'meta': expected.meta,
        }

    def serialize_category(self, category: Category):
        return CategoryResource.category_to_response(category)['data']
