#pylint: disable=unexpected-keyword-arg
import pytest
from rest_framework.exceptions import ErrorDetail, ValidationError
from django_app import container
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.api import CategoryResource
from core.category.tests.helpers import init_category_resource_all_none
from core.__seedwork.domain.exceptions import NotFoundException
from core.category.tests.fixture.categories_api_fixture import (
    CategoryApiFixture
)


@pytest.mark.django_db
class TestCategoryResourceGetObjectMethodInt:

    resource: CategoryResource
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = container.repository_category_django_orm()
        cls.resource = CategoryResource(**{
            **init_category_resource_all_none(),
            'get_use_case': container.use_case_category_get_category
        })

    def test_throw_exception_when_uuid_is_invalid(self):
        with pytest.raises(ValidationError) as assert_exception:
            self.resource.get_object('fake api')
        assert assert_exception.value.detail == {
            'id': [ErrorDetail(string='Must be a valid UUID.', code='invalid')]
        }

    def test_throw_exception_when_category_not_found(self):
        uuid_value = 'af46842e-027d-4c91-b259-3a3642144ba4'
        with pytest.raises(NotFoundException) as assert_exception:
            self.resource.get_object(uuid_value)
        error_message = assert_exception.value.args[0]
        assert error_message == f"Entity not found using ID '{uuid_value}'"

    def test_get_object_method(self):
        category = Category.fake().a_category().build()
        self.repo.insert(category)

        response = self.resource.get_object(category.id)

        assert response.status_code == 200
        assert 'data' in response.data
        serialized = CategoryResource.category_to_response(category)
        assert CategoryApiFixture.keys_in_category_response() == list(response.data['data'].keys())
        assert response.data == serialized

        assert response.data == {
            'data': {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'is_active': category.is_active,
                'created_at': serialized['data']['created_at']
            }
        }
