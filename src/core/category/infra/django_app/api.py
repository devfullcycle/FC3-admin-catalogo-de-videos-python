from typing import Callable
from dataclasses import dataclass
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request as DrfRequest
from rest_framework import status as http
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
    GetCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)
from core.category.infra.django_app.serializers import (
    CategoryCollectionSerializer,
    CategorySerializer
)
from core.category.application.dto import CategoryOutput
from core.__seedwork.infra.django_app.serializers import UUIDSerializer
# testes end to end - funcionamento
# testes integração -
# testes unitários controllers -


@dataclass(slots=True)
class CategoryResource(APIView):

    create_use_case: Callable[[], CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]
    get_use_case: Callable[[], GetCategoryUseCase]
    update_use_case: Callable[[], UpdateCategoryUseCase]
    delete_use_case: Callable[[], DeleteCategoryUseCase]

    def post(self, request: DrfRequest):

        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_param = CreateCategoryUseCase.Input(**serializer.validated_data)
        output = self.create_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output)
        return Response(body, status=http.HTTP_201_CREATED)

    def get(self, request: DrfRequest, id: str = None):  # pylint: disable=redefined-builtin,invalid-name
        if id:
            return self.get_object(id)

        input_param = ListCategoriesUseCase.Input(
            **request.query_params.dict()
        )
        output = self.list_use_case().execute(input_param)
        data = CategoryCollectionSerializer(instance=output).data
        return Response(data)

    def get_object(self, id: str):  # pylint: disable=redefined-builtin,invalid-name
        CategoryResource.validate_id(id)
        input_param = GetCategoryUseCase.Input(id)
        output = self.get_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output)
        return Response(body)

    def put(self, request: DrfRequest, id: str):
        CategoryResource.validate_id(id)

        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # pylint: disable=redefined-builtin,invalid-name
        input_param = UpdateCategoryUseCase.Input(
            **{
                'id': id,
                **serializer.validated_data
            }
        )
        output = self.update_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output)
        return Response(body)

    def delete(self, _request: DrfRequest, id: str):  # pylint: disable=redefined-builtin,invalid-name
        CategoryResource.validate_id(id)
        input_param = DeleteCategoryUseCase.Input(id=id)
        self.delete_use_case().execute(input_param)
        return Response(status=http.HTTP_204_NO_CONTENT)

    @staticmethod
    def category_to_response(output: CategoryOutput):
        serializer = CategorySerializer(instance=output)
        return serializer.data

    @staticmethod
    def validate_id(id: str):  # pylint: disable=redefined-builtin,invalid-name
        serializer = UUIDSerializer(data={'id': id})
        serializer.is_valid(raise_exception=True)
