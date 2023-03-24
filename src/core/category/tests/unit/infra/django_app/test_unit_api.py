from collections import namedtuple
from datetime import datetime
import unittest
from unittest import mock
from core.__seedwork.infra.django_app.serializers import UUIDSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request as DrfRequest
from core.category.infra.django_app.api import CategoryResource
from core.category.infra.django_app.serializers import CategorySerializer
from core.category.application.dto import CategoryOutput
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
    GetCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)
from core.category.tests.helpers import init_category_resource_all_none
from core.__seedwork.infra.testing.helpers import make_request

class StubCategorySerializer:

    validated_data = None

    def is_valid(self, raise_exception: bool):
        pass


class TestCategoryResourceUnit(unittest.TestCase):

    @mock.patch.object(
        CategorySerializer,
        '__new__'
    )
    def test_category_to_response_method(self, mock_serializer):
        mock_serializer.return_value = namedtuple(
            'Faker', ['data'])(data='test')
        data = CategoryResource.category_to_response('output')
        mock_serializer.assert_called_with(
            CategorySerializer, 
            instance='output'
        )
        self.assertEqual(data, 'test')

    @mock.patch.object(
        UUIDSerializer,
        '__new__'
    )
    def test_validate_id_method(self, mock_serializer):
        mock_serializer_is_valid = mock.MagicMock()
        mock_serializer.return_value = namedtuple(
            'Fake', ['is_valid'])\
            (is_valid=mock_serializer_is_valid)
        CategoryResource.validate_id('fake id')
        mock_serializer.assert_called_with(
            UUIDSerializer,
            data={'id': 'fake id'}
        )
        mock_serializer_is_valid.assert_called_with(
            raise_exception=True
        )

    @mock.patch.object(CategoryResource, 'category_to_response')
    def test_post_method(self, mock_category_to_response):
        stub_serializer = StubCategorySerializer()
        send_data = {'name': 'Movie'}
        expected_response = {
            'id': 'af46842e-027d-4c91-b259-3a3642144ba4',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': datetime.now()
        }
        with mock.patch.object(
            CategorySerializer,
            '__new__',
            return_value=stub_serializer
        ) as mock_serializer:

            stub_serializer.validated_data = send_data
            stub_serializer.is_valid = mock.MagicMock()

            mock_create_use_case = mock.Mock(CreateCategoryUseCase)
            mock_create_use_case.execute.return_value = CreateCategoryUseCase.Output(
                **expected_response
            )

            mock_category_to_response.return_value = expected_response

            resource = CategoryResource(
                ** {
                    **init_category_resource_all_none(),
                    'create_use_case': lambda: mock_create_use_case
                }
            )
            request = make_request('post', send_data=send_data)       
            response = resource.post(request)
            stub_serializer.is_valid.assert_called_with(raise_exception=True)
            mock_create_use_case.execute.assert_called_with(CreateCategoryUseCase.Input(
                name='Movie'
            ))
            mock_category_to_response.assert_called_with(
                mock_create_use_case.execute.return_value
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data, {
                'id': 'af46842e-027d-4c91-b259-3a3642144ba4',
                'name': 'Movie',
                'description': None,
                'is_active': True,
                'created_at': expected_response['created_at']
            })
        mock_serializer.assert_called_with(CategorySerializer, data=send_data)

    def test_get_method(self):
        mock_list_use_case = mock.Mock(CreateCategoryUseCase)

        mock_list_use_case.execute.return_value = ListCategoriesUseCase.Output(
            items=[
                CategoryOutput(
                    id='af46842e-027d-4c91-b259-3a3642144ba4',
                    name='Movie',
                    description=None,
                    is_active=True,
                    created_at=datetime.now()
                )
            ],
            total=1,
            current_page=1,
            per_page=2,
            last_page=1
        )

        resource = CategoryResource(**{
            **init_category_resource_all_none(),
            'list_use_case': lambda: mock_list_use_case,
        })
        _request = APIRequestFactory().get(
            '/?page=1&per_page=1&sort=name&sort_dir=asc&filter=test')
        request = DrfRequest(_request)
        response = resource.get(request)
        mock_list_use_case.execute.assert_called_with(ListCategoriesUseCase.Input(
            page='1',
            per_page='1',
            sort='name',
            sort_dir='asc',
            filter='test'
        ))
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data, {
        #     'items': [
        #         {
        #             'id': 'af46842e-027d-4c91-b259-3a3642144ba4',
        #             'name': 'Movie',
        #             'description': None,
        #             'is_active': True,
        #             'created_at': mock_list_use_case.execute.return_value.items[0].created_at
        #         }
        #     ],
        #     'total': 1,
        #     'current_page': 1,
        #     'per_page': 2,
        #     'last_page': 1,
        # })

    def test_if_get_invoke_get_object(self):
        resource = CategoryResource(**init_category_resource_all_none())
        resource.get_object = mock.Mock()
        resource.get(None, 'af46842e-027d-4c91-b259-3a3642144ba4')
        resource.get_object.assert_called_with(
            'af46842e-027d-4c91-b259-3a3642144ba4')
        # mock_list_use_case = mock.Mock(ListCategoriesUseCase)
        # mock_get_use_case = mock.Mock(GetCategoryUseCase)

        # mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
        #     id='af46842e-027d-4c91-b259-3a3642144ba4',
        #     name='Movie',
        #     description=None,
        #     is_active=True,
        #     created_at=datetime.now()
        # )

        # resource = CategoryResource(
        #     ** {
        #         **self.__init_all_none(),
        #         'list_use_case': lambda: list_get_use_case,
        #         'get_use_case': lambda: mock_get_use_case
        #     }
        # )
        # response = resource.get(None, 'af46842e-027d-4c91-b259-3a3642144ba4')
        # self.assertEqual(mock_list_use_case.call_count, 0)
        # mock_get_use_case.execute.assert_called_with(GetCategoryUseCase.Input(
        #     id='af46842e-027d-4c91-b259-3a3642144ba4'
        # ))
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data, {
        #     'id': 'af46842e-027d-4c91-b259-3a3642144ba4',
        #     'name': 'Movie',
        #     'description': None,
        #     'is_active': True,
        #     'created_at': mock_get_use_case.execute.return_value.created_at
        # })

    @mock.patch.object(CategoryResource, 'category_to_response')
    @mock.patch.object(CategoryResource, 'validate_id')
    def test_get_object_method(self, mock_validate_id, mock_category_to_response):
        expected_response = {
            'id': 'af46842e-027d-4c91-b259-3a3642144ba4',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': datetime.now()
        }
        mock_get_use_case = mock.Mock(GetCategoryUseCase)
        mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
            **expected_response
        )
        mock_category_to_response.return_value = {
            **expected_response,
        }

        resource = CategoryResource(
            ** {
                **init_category_resource_all_none(),
                'get_use_case': lambda: mock_get_use_case
            }
        )
        uuid_value = 'af46842e-027d-4c91-b259-3a3642144ba4'
        response = resource.get_object(uuid_value)
        mock_validate_id.assert_called_with(uuid_value)
        mock_get_use_case.execute.assert_called_with(GetCategoryUseCase.Input(
            id=uuid_value
        ))
        mock_category_to_response.assert_called_with(
            mock_get_use_case.execute.return_value
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch.object(CategoryResource, 'category_to_response')
    @mock.patch.object(CategoryResource, 'validate_id')
    def test_put_method(self, mock_validate_id, mock_category_to_response):
        send_data = {
            'id': 'af46842e-027d-4c91-b259-3a3642144ba4',
            'name': 'Movie'
        }
        mock_update_use_case = mock.Mock(UpdateCategoryUseCase)
        mock_update_use_case.execute.return_value = UpdateCategoryUseCase.Output(
            id=send_data['id'],
            name=send_data['name'],
            description=None,
            is_active=True,
            created_at=datetime.now()
        )
        expected_response = {
            'id': send_data['id'],
            'name': send_data['name'],
            'description': None,
            'is_active': True,
            'created_at': mock_update_use_case.execute.return_value.created_at
        }

        mock_category_to_response.return_value = expected_response

        resource = CategoryResource(
            ** {
                **init_category_resource_all_none(),
                'update_use_case': lambda: mock_update_use_case
            }
        )
        request = make_request('put',send_data=send_data)
        response = resource.put(request, send_data['id'])
        mock_validate_id.assert_called_with(send_data['id'])
        mock_update_use_case.execute.assert_called_with(UpdateCategoryUseCase.Input(
            id=send_data['id'],
            name=send_data['name']
        ))
        mock_category_to_response.assert_called_with(
                mock_update_use_case.execute.return_value
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch.object(CategoryResource, 'validate_id')
    def test_delete_method(self, mock_validate_id):
        mock_delete_use_case = mock.Mock(DeleteCategoryUseCase)

        resource = CategoryResource(
            ** {
                **init_category_resource_all_none(),
                'delete_use_case': lambda: mock_delete_use_case
            }
        )
        _request = APIRequestFactory().delete('/')
        request = DrfRequest(_request)
        uuid_value = 'af46842e-027d-4c91-b259-3a3642144ba4'
        response = resource.delete(request, uuid_value)
        mock_validate_id.assert_called_with(uuid_value)
        mock_delete_use_case.execute.assert_called_with(DeleteCategoryUseCase.Input(
            id=uuid_value
        ))
        self.assertEqual(response.status_code, 204)
