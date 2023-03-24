from core.__seedwork.infra.django_app.serializers import ISO_8601
import pytest
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail, ValidationError

from core.category.application.dto import CategoryOutput
from core.category.infra.django_app.api import CategoryResource
from core.category.tests.helpers import init_category_resource_all_none


@pytest.mark.django_db()
class TestCategoryResourceCommonMethodsInt:

    category_resource: CategoryResource

    @classmethod
    def setup_class(cls):
        cls.category_resource = CategoryResource(
            **init_category_resource_all_none()
        )

    def test_category_to_response(self):
        output = CategoryOutput(
            id='fake id',
            name='category test',
            description='description test',
            is_active=True,
            created_at=timezone.now()
        )
        data = CategoryResource.category_to_response(output)
        assert data == {
            'data': {
                'id': 'fake id',
                'name': 'category test',
                'description': 'description test',
                'is_active': True,
                'created_at': output.created_at.strftime(ISO_8601)
            }

        }

    def test_validate_id(self):
        with pytest.raises(ValidationError) as assert_exception:
            CategoryResource.validate_id('fake')

        assert assert_exception.value.detail == {
            'id': [ErrorDetail(string='Must be a valid UUID.', code='invalid')]
        }
