from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category
from core.category.infra.django_app.api import CategoryResource
import pytest
from django_app import container
from core.category.domain.repositories import CategoryRepository
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient

@pytest.mark.group('e2e')
@pytest.mark.django_db
class TestCategoriesGetObjectE2E:

    client_http: APIClient
    category_repository: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.client_http = APIClient()
        cls.category_repository = container.repository_category_django_orm()

    def test_invalid_request(self):
        unique_id = UniqueEntityId().id
        arrange = [
            {
                'id': unique_id,
                'expected': {
                    'status_code': 404,
                    'response': {
                        'message': f"Entity not found using ID '{unique_id}'"
                    }
                }
            },
            {
                'id': 'fake id',
                'expected': {
                    'status_code': 422,
                    'response': {
                        'id': ['Must be a valid UUID.']
                    }
                }
            }
        ]

        for item in arrange:
            response = self.client_http.get(
                f'/categories/{item["id"]}/', format='json')
            assert response.status_code == item['expected']['status_code']
            print(response.content)
            assert response.content == JSONRenderer().render(
                item['expected']['response'])

    def test_get_object(self):
        category_created = Category.fake().a_category().build()
        self.category_repository.insert(category_created)
        response = self.client_http.get(
            f'/categories/{category_created.id}/', format='json')

        assert response.status_code == 200
        json_serialized = CategoryResource.category_to_response(
            category_created)
        assert response.content == JSONRenderer().render(json_serialized)
