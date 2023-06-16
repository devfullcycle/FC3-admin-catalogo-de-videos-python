
from collections import namedtuple
from dataclasses import dataclass
import datetime
from typing import Any, Optional
import pytest
from rest_framework.exceptions import ErrorDetail, ValidationError
from core.category.domain.entities import Category
from core.__seedwork.domain.exceptions import EntityValidationException


@dataclass
class Request:
    body: Any


@dataclass
class Response:
    body: Any


@dataclass
class HttpExpect:
    request: Request
    response: Optional[Response] = None
    exception: Optional[Exception] = None


@dataclass
class CategoryInvalidBodyFixture:
    body_empty: HttpExpect
    name_none: HttpExpect
    name_empty: HttpExpect
    name_not_a_str: HttpExpect
    description_not_a_str: HttpExpect
    is_active_none: HttpExpect
    is_active_empty: HttpExpect
    is_active_not_a_bool: HttpExpect

    @staticmethod
    def arrange():
        faker = Category.fake().a_category()
        return CategoryInvalidBodyFixture(
            body_empty=HttpExpect(
                request=Request(body={}),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field is required.', 'required')
                    ],
                })
            ),
            name_none=HttpExpect(  # vai acontecer um erro
                request=Request(
                    body={'name': faker.with_invalid_name_none().name}),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field may not be null.', 'null')
                    ],
                })),
            name_empty=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_empty().name}),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field may not be blank.', 'blank')
                    ],
                })),
            name_not_a_str=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_not_a_string().name}),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('Not a valid string', 'invalid')
                    ],
                })),
            description_not_a_str=HttpExpect(
                request=Request(
                    body={
                        'description': faker.with_invalid_description_not_a_string().description
                    }
                ),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field is required.', 'required')
                    ],
                    'description': [
                        ErrorDetail('Not a valid string', 'invalid')
                    ],
                })),
            is_active_none=HttpExpect(
                request=Request(
                    body={
                        'is_active': faker.with_invalid_is_active_none().is_active
                    }
                ),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field is required.', 'required')
                    ],
                    'is_active': [
                        ErrorDetail('This field may not be null.', 'null')
                    ],
                })),
            is_active_empty=HttpExpect(
                request=Request(
                    body={
                        'is_active': faker.with_invalid_is_active_empty().is_active
                    }
                ),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field is required.', 'required')
                    ],
                    'is_active': [
                        ErrorDetail('Must be a valid boolean.', 'invalid')
                    ],
                })),
            is_active_not_a_bool=HttpExpect(
                request=Request(
                    body={
                        'is_active': faker.with_invalid_is_active_not_a_boolean().is_active
                    }
                ),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field is required.', 'required')
                    ],
                    'is_active': [
                        ErrorDetail('Must be a valid boolean.', 'invalid')
                    ],
                })),
        )


@dataclass
class CategoryEntityValidationErrorFixture:
    name_none: HttpExpect
    name_empty: HttpExpect
    name_not_a_str: HttpExpect
    name_too_long: HttpExpect
    description_not_a_str: HttpExpect
    is_active_none: HttpExpect
    is_active_empty: HttpExpect
    is_active_not_a_bool: HttpExpect

    @staticmethod
    def arrange():
        faker = Category.fake().a_category()
        return CategoryEntityValidationErrorFixture(
            name_none=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_none().name}),
                exception=EntityValidationException({
                    'name': [
                        'This field may not be null.'
                    ],
                })),
            name_empty=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_empty().name}),
                exception=EntityValidationException({
                    'name': [
                        'This field may not be blank.'
                    ],
                })),
            name_not_a_str=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_not_a_string().name}),
                exception=EntityValidationException({
                    'name': [
                        'Not a valid string.'
                    ],
                })),
            name_too_long=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_too_long().name}),
                exception=EntityValidationException({
                    'name': [
                        'Ensure this field has no more than 255 characters.'
                    ],
                })),
            description_not_a_str=HttpExpect(
                request=Request(
                    body={
                        'name': faker.with_invalid_name_none().name,
                        'description': faker.with_invalid_description_not_a_string().description
                    }
                ),
                exception=EntityValidationException({
                    'name': [
                        'This field may not be null.'
                    ],
                    'description': [
                        'Not a valid string.'
                    ],
                })),
            is_active_none=HttpExpect(
                request=Request(
                    body={
                        'name': faker.with_invalid_name_none().name,
                        'is_active': faker.with_invalid_is_active_none().is_active
                    }
                ),
                exception=EntityValidationException({
                    'name': [
                        'This field may not be null.'
                    ],
                    'is_active': [
                        'This field may not be null.'
                    ],
                })),
            is_active_empty=HttpExpect(
                request=Request(
                    body={
                        'name': faker.with_invalid_name_none().name,
                        'is_active': faker.with_invalid_is_active_empty().is_active
                    }
                ),
                exception=EntityValidationException({
                    'name': [
                        'This field may not be null.'
                    ],
                    'is_active': [
                        'Must be a valid boolean.'
                    ],
                })),
            is_active_not_a_bool=HttpExpect(
                request=Request(
                    body={
                        'name': faker.with_invalid_name_none().name,
                        'is_active': faker.with_invalid_is_active_not_a_boolean().is_active
                    }
                ),
                exception=EntityValidationException({
                    'name': [
                        'This field may not be null.'
                    ],
                    'is_active': [
                        'Must be a valid boolean.'
                    ],
                })),
        )


class CategoryApiFixture:

    @staticmethod
    def keys_in_category_response():
        return ['id', 'name', 'description', 'is_active', 'created_at']


class CreateCategoryApiFixture:

    @staticmethod
    def arrange_for_invalid_requests():
        fixture = CategoryInvalidBodyFixture.arrange()
        return [
            pytest.param(fixture.body_empty, id='body_empty'),
            pytest.param(fixture.name_none, id='name_none'),
            pytest.param(fixture.name_empty, id='name_empty'),
            pytest.param(fixture.is_active_none, id='is_active_none'),
            pytest.param(fixture.is_active_empty, id='is_active_empty'),
            pytest.param(fixture.is_active_not_a_bool,
                         id='is_active_not_a_bool'),
        ]

    @staticmethod
    def arrange_for_entity_validation_error():
        fixture = CategoryEntityValidationErrorFixture.arrange()
        return [
            pytest.param(fixture.name_empty, id='name_empty'),
            pytest.param(fixture.name_none, id='name_none'),
            pytest.param(fixture.name_not_a_str, id='name_not_a_str'),
            pytest.param(fixture.name_too_long, id='name_too_long'),
            pytest.param(fixture.description_not_a_str,
                         id='description_not_a_str'),
            pytest.param(fixture.is_active_empty, id='is_active_empty'),
            pytest.param(fixture.is_active_not_a_bool,
                         id='is_active_not_a_bool'),
        ]

    @staticmethod
    def keys_in_category_response():
        return CategoryApiFixture.keys_in_category_response()

    @staticmethod
    def arrange_for_save():
        faker = Category.fake().a_category()\
            .with_name('Movie')\
            .with_description('description test')

        data = [
            HttpExpect(
                request=Request(body={'name': faker.name}),
                response=Response(body={
                    'name': faker.name,
                    'description': None,
                    'is_active': True,
                })
            ),
            HttpExpect(
                request=Request(body={
                    'name': faker.name,
                    'description': faker.description,
                }),
                response=Response(body={
                    'name': faker.name,
                    'description': faker.description,
                    'is_active': True,
                })
            ),
            HttpExpect(
                request=Request(body={
                    'name': faker.name,
                    'is_active': True
                }),
                response=Response(body={
                    'name': faker.name,
                    'description': None,
                    'is_active': True,
                })
            ),
            HttpExpect(
                request=Request(body={
                    'name': faker.name,
                    'is_active': False
                }),
                response=Response(body={
                    'name': faker.name,
                    'description': None,
                    'is_active': False,
                })
            )
        ]
        return [pytest.param(item, id=str(item.request.body)) for item in data]


class UpdateCategoryApiFixture:

    @staticmethod
    def arrange_for_invalid_requests():
        fixture = CategoryInvalidBodyFixture.arrange()
        return [
            pytest.param(fixture.body_empty, id='body_empty'),
            pytest.param(fixture.name_none, id='name_none'),
            pytest.param(fixture.name_empty, id='name_empty'),
            pytest.param(fixture.is_active_none, id='is_active_none'),
            pytest.param(fixture.is_active_empty, id='is_active_empty'),
            pytest.param(fixture.is_active_not_a_bool,
                         id='is_active_not_a_bool'),
        ]

    @staticmethod
    def arrange_for_entity_validation_error():
        fixture = CategoryEntityValidationErrorFixture.arrange()
        return [
            pytest.param(fixture.name_empty, id='name_empty'),
            pytest.param(fixture.name_none, id='name_none'),
            pytest.param(fixture.name_not_a_str, id='name_not_a_str'),
            pytest.param(fixture.name_too_long, id='name_too_long'),
            pytest.param(fixture.description_not_a_str,
                         id='description_not_a_str')
        ]

    @staticmethod
    def keys_in_category_response():
        return CategoryApiFixture.keys_in_category_response()

    @staticmethod
    def arrange_for_save():
        data = [
            HttpExpect(
                request=Request(body={'name': "Movie"}),
                response=Response(body={
                    'name': 'Movie',
                    'description': None,
                    'is_active': True,
                })
            ),
            HttpExpect(
                request=Request(
                    body={'name': "Movie", "description": "test description"}),
                response=Response(body={
                    'name': 'Movie',
                    'description': "test description",
                    'is_active': True,
                })
            ),
            HttpExpect(
                request=Request(body={'name': "Movie", "is_active": False}),
                response=Response(body={
                    'name': 'Movie',
                    'description': None,
                    'is_active': False,
                })
            ),
            HttpExpect(
                request=Request(body={'name': "Movie", "is_active": True}),
                response=Response(body={
                    'name': 'Movie',
                    'description': None,
                    'is_active': True,
                })
            ),
        ]

        return [pytest.param(item, id=str(item.request.body)) for item in data]


@dataclass
class SearchExpectation:
    send_data: dict
    expected: 'SearchExpectation.Expected'
    entities: list

    @dataclass
    class Expected:
        entities: list
        meta: dict


class ListCategoriesApiFixture:

    @staticmethod
    def arrange_incremented_with_created_at():
        def with_created_at_faker(index):
            return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=index)
        categories = Category.fake()\
            .the_categories(4)\
            .with_created_at(with_created_at_faker).build()

        CategoriesNamed = namedtuple(
            'CategoriesNamed', ['first', 'second', 'third', 'fourth'])
        categories_named = CategoriesNamed(
            first=categories[0],
            second=categories[1],
            third=categories[2],
            fourth=categories[3],
        )

        arrange = [
            SearchExpectation(
                send_data={},
                expected=SearchExpectation.Expected(
                    entities=[
                        categories_named.fourth,
                        categories_named.third,
                        categories_named.second,
                        categories_named.first
                    ],
                    meta={'total': 4, 'current_page': 1, 'per_page': 15, 'last_page': 1}
                ),
                entities=categories
            ),
            SearchExpectation(
                send_data={'page': 1, 'per_page': 2},
                expected=SearchExpectation.Expected(
                    entities=[categories_named.fourth, categories_named.third],
                    meta={'total': 4, 'current_page': 1, 'per_page': 2, 'last_page': 2}
                ),
                entities=categories
            ),
            SearchExpectation(
                send_data={'page': 2, 'per_page': 2},
                expected=SearchExpectation.Expected(
                    entities=[categories_named.second, categories_named.first],
                    meta={'total': 4, 'current_page': 2, 'per_page': 2, 'last_page': 2}
                ),
                entities=categories
            ),
        ]

        return [pytest.param(item, id=f'send_data={str(item.send_data)}') for item in arrange]
    
    @staticmethod
    def arrange_unsorted():
        faker = Category.fake().a_category()
        categories = [
            faker.with_name('a').build(),
            faker.with_name('AAA').build(),
            faker.with_name('AaA').build(),
            faker.with_name('b').build(),
            faker.with_name('c').build(),
        ]
        CategoriesNamed = namedtuple('CategoriesNamed', ['a', 'AAA', 'AaA', 'b', 'c'])
        categories_named = CategoriesNamed(
            a=categories[0],
            AAA=categories[1],
            AaA=categories[2],
            b=categories[3],
            c=categories[4],
        )
        arrange = [
            SearchExpectation(
                send_data={
                    'page': 1,
                    'per_page': 2,
                    'sort': 'name',
                    'filter': 'a'
                },
                expected=SearchExpectation.Expected(
                    entities=[
                        categories_named.AAA,
                        categories_named.AaA,
                    ],
                    meta={
                        'total': 3,
                        'current_page': 1,
                        'per_page': 2,
                        'last_page': 2,
                    }
                ),
                entities=categories
            ),
            SearchExpectation(
                send_data={
                    'page': 2,
                    'per_page': 2,
                    'sort': 'name',
                    'filter': 'a'
                },
                expected=SearchExpectation.Expected(
                    entities=[
                        categories_named.a,
                    ],
                    meta={
                        'total': 3,
                        'current_page': 2,
                        'per_page': 2,
                        'last_page': 2
                    }
                ),
                entities=categories
            )
        ]

        return [pytest.param(item, id=f'send_data={str(item.send_data)}') for item in arrange]
