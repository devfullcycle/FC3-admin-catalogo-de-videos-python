# pylint: disable=unexpected-keyword-arg
from datetime import datetime, timedelta
from typing import Optional
import unittest
from unittest.mock import patch
from core.__seedwork.application.dto import PaginationOutput, PaginationOutputMapper, SearchInput
from core.__seedwork.application.use_cases import UseCase
from core.__seedwork.domain.exceptions import NotFoundException
from core.category.application.dto import CategoryOutput, CategoryOutputMapper

from core.category.application.use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase
)
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository


class TestCreateCategoryUseCaseUnit(unittest.TestCase):

    use_case: CreateCategoryUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(self.category_repo)

    def test_if_instance_a_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(CreateCategoryUseCase.Input.__annotations__, {
            'name': str,
            'description': Optional[str],
            'is_active': Optional[bool],
        })
        # pylint: disable=no-member
        description_field = CreateCategoryUseCase.Input.__dataclass_fields__[
            'description']
        self.assertEqual(description_field.default,
                         Category.get_field('description').default)

        is_active_field = CreateCategoryUseCase.Input.__dataclass_fields__[
            'is_active']
        self.assertEqual(is_active_field.default,
                         Category.get_field('is_active').default)

    def test_output(self):
        self.assertTrue(
            issubclass(
                CreateCategoryUseCase.Output,
                CategoryOutput
            )
        )

    def test_execute(self):
        with patch.object(
            self.category_repo,
            'insert',
            wraps=self.category_repo.insert
        ) as spy_insert:
            input_param = CreateCategoryUseCase.Input(name='Movie')
            output = self.use_case.execute(input_param)
            spy_insert.assert_called_once()
            self.assertEqual(output, CreateCategoryUseCase.Output(
                id=self.category_repo.items[0].id,
                name='Movie',
                description=None,
                is_active=True,
                created_at=self.category_repo.items[0].created_at
            ))

        input_param = CreateCategoryUseCase.Input(
            name='Movie', description='some description', is_active=False)
        output = self.use_case.execute(input_param)
        self.assertEqual(output, CreateCategoryUseCase.Output(
            id=self.category_repo.items[1].id,
            name='Movie',
            description='some description',
            is_active=False,
            created_at=self.category_repo.items[1].created_at
        ))

        input_param = CreateCategoryUseCase.Input(
            name='Movie', description='some description', is_active=True)
        output = self.use_case.execute(input_param)
        self.assertEqual(output, CreateCategoryUseCase.Output(
            id=self.category_repo.items[2].id,
            name='Movie',
            description='some description',
            is_active=True,
            created_at=self.category_repo.items[2].created_at
        ))


class TestGetCategoryUseCaseUnit(unittest.TestCase):

    use_case: GetCategoryUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = GetCategoryUseCase(self.category_repo)

    def test_if_instance_a_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(GetCategoryUseCase.Input.__annotations__, {
            'id': str,
        })

    def test_throws_exception_when_category_not_found(self):
        input_param = GetCategoryUseCase.Input('fake id')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param)
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake id'")

    def test_output(self):
        self.assertTrue(
            issubclass(
                GetCategoryUseCase.Output,
                CategoryOutput
            )
        )

    def test_execute(self):
        category = Category(name='Movie')
        self.category_repo.items = [category]
        with patch.object(
            self.category_repo,
            'find_by_id',
            wraps=self.category_repo.find_by_id
        ) as spy_find_by_id:
            input_param = GetCategoryUseCase.Input(category.id)
            output = self.use_case.execute(input_param)
            spy_find_by_id.assert_called_once()
            self.assertEqual(output, GetCategoryUseCase.Output(
                id=self.category_repo.items[0].id,
                name='Movie',
                description=None,
                is_active=True,
                created_at=self.category_repo.items[0].created_at
            ))


class TestListCategoriesUseCase(unittest.TestCase):

    use_case: ListCategoriesUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = ListCategoriesUseCase(self.category_repo)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertTrue(issubclass(
            ListCategoriesUseCase.Input, SearchInput))

    def test_output(self):
        self.assertTrue(issubclass(
            ListCategoriesUseCase.Output, PaginationOutput))

    def test__to_output(self):
        entity = Category(name='Movie')
        default_props = {
            'total': 1,
            'current_page': 1,
            'per_page': 2,
            'sort': None,
            'sort_dir': None,
            'filter': None
        }

        result = CategoryRepository.SearchResult(items=[], **default_props)
        output = self.use_case._ListCategoriesUseCase__to_output(  # pylint: disable=protected-access
            result
        )
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=[],
            total=1,
            current_page=1,
            per_page=2,
            last_page=1,
        ))

        result = CategoryRepository.SearchResult(
            items=[entity], **default_props)
        output = self.use_case._ListCategoriesUseCase__to_output(  # pylint: disable=protected-access
            result
        )
        items = [CategoryOutputMapper.without_child().to_output(entity)]
        self.assertEqual(
            output,
            PaginationOutputMapper
            .from_child(ListCategoriesUseCase.Output)
            .to_output(
                items,
                result
            ))

    def test_execute_using_empty_search_params(self):
        self.category_repo.items = [
            Category(name='test 1'),
            Category(name='test 2', created_at=datetime.now() +
                     timedelta(seconds=200)),
        ]
        with patch.object(
            self.category_repo,
            'search',
            wraps=self.category_repo.search
        ) as spy_search:
            input_param = ListCategoriesUseCase.Input()
            output = self.use_case.execute(input_param)
            spy_search.assert_called_once()
            self.assertEqual(output, ListCategoriesUseCase.Output(
                items=list(
                    map(
                        CategoryOutputMapper.without_child().to_output,
                        self.category_repo.items[::-1]
                    )
                ),
                total=2,
                current_page=1,
                per_page=15,
                last_page=1
            ))

    def test_execute_using_pagination_and_sort_and_filter(self):
        items = [
            Category(name='a'),
            Category(name='AAA'),  # asci
            Category(name='AaA'),
            Category(name='b'),
            Category(name='c'),
        ]
        self.category_repo.items = items

        input_param = ListCategoriesUseCase.Input(
            page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.without_child().to_output,
                    [items[1], items[2]]
                )
            ),
            total=3,
            current_page=1,
            per_page=2,
            last_page=2
        ))

        input_param = ListCategoriesUseCase.Input(
            page=2,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.without_child().to_output,
                    [items[0]]
                )
            ),
            total=3,
            current_page=2,
            per_page=2,
            last_page=2
        ))

        input_param = ListCategoriesUseCase.Input(
            page=1,
            per_page=2,
            sort='name',
            sort_dir='desc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.without_child().to_output,
                    [items[0], items[2]]
                )
            ),
            total=3,
            current_page=1,
            per_page=2,
            last_page=2
        ))

        input_param = ListCategoriesUseCase.Input(
            page=2,
            per_page=2,
            sort='name',
            sort_dir='desc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.without_child().to_output,
                    [items[1]]
                )
            ),
            total=3,
            current_page=2,
            per_page=2,
            last_page=2
        ))


class TestUpdateCategoryUseCase(unittest.TestCase):

    use_case: UpdateCategoryUseCase
    category_repo: CategoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = UpdateCategoryUseCase(self.category_repo)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(UpdateCategoryUseCase.Input.__annotations__, {
            'id': str,
            'name': str,
            'description': Optional[str],
            'is_active': Optional[bool]
        })
        # pylint: disable=no-member
        description_field = UpdateCategoryUseCase.Input.__dataclass_fields__[
            'description']
        self.assertEqual(description_field.default,
                         Category.get_field('description').default)

        is_active_field = UpdateCategoryUseCase.Input.__dataclass_fields__[
            'is_active']
        self.assertEqual(is_active_field.default,
                         Category.get_field('is_active').default)

    def test_output(self):
        self.assertTrue(issubclass(
            UpdateCategoryUseCase.Output, CategoryOutput))

    def test_throw_exception_when_category_not_found(self):
        request = UpdateCategoryUseCase.Input(id='not_found', name='test')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(request)
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'not_found'")

    def test_execute(self):
        category = Category(name='test')
        self.category_repo.items = [category]
        with patch.object(
            self.category_repo,
            'update',
            wraps=self.category_repo.update
        ) as spy_update:
            request = UpdateCategoryUseCase.Input(
                id=category.id,
                name='test 1',
            )
            response = self.use_case.execute(request)
            spy_update.assert_called_once()
            self.assertEqual(response, UpdateCategoryUseCase.Output(
                id=category.id,
                name='test 1',
                description=None,
                is_active=True,
                created_at=category.created_at
            ))

        arrange = [
            {
                'input': {
                    'id': category.id,
                    'name': 'test 2',
                    'description': 'test description',
                },
                'expected': {
                    'id': category.id,
                    'name': 'test 2',
                    'description': 'test description',
                    'is_active': True,
                    'created_at': category.created_at
                }
            },
            {
                'input': {
                    'id': category.id,
                    'name': 'test',
                },
                'expected': {
                    'id': category.id,
                    'name': 'test',
                    'description': None,
                    'is_active': True,
                    'created_at': category.created_at
                }
            },
            {
                'input': {
                    'id': category.id,
                    'name': 'test',
                    'is_active': False,
                },
                'expected': {
                    'id': category.id,
                    'name': 'test',
                    'description': None,
                    'is_active': False,
                    'created_at': category.created_at
                }
            },
            {
                'input': {
                    'id': category.id,
                    'name': 'test',
                    'is_active': True
                },
                'expected': {
                    'id': category.id,
                    'name': 'test',
                    'description': None,
                    'is_active': True,
                    'created_at': category.created_at
                }
            },
            {
                'input': {
                    'id': category.id,
                    'name': 'test',
                    'description': 'test description',
                    'is_active': False
                },
                'expected': {
                    'id': category.id,
                    'name': 'test',
                    'description': 'test description',
                    'is_active': False,
                    'created_at': category.created_at
                }
            }
        ]

        for i in arrange:
            request = UpdateCategoryUseCase.Input(**i['input'])
            response = self.use_case.execute(request)
            self.assertEqual(
                response,
                UpdateCategoryUseCase.Output(**i['expected'])
            )


class TestDeleteCategoryUseCase(unittest.TestCase):

    use_case: DeleteCategoryUseCase
    category_repo: CategoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = DeleteCategoryUseCase(self.category_repo)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(DeleteCategoryUseCase.Input.__annotations__, {
            'id': str
        })

    def test_throw_exception_when_category_not_found(self):
        request = DeleteCategoryUseCase.Input(id='not_found')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(request)
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'not_found'")

    def test_execute(self):
        category = Category(name='test')
        self.category_repo.items = [category]
        with patch.object(
            self.category_repo,
            'delete',
            wraps=self.category_repo.delete
        ) as spy_delete:
            request = DeleteCategoryUseCase.Input(id=category.id)
            self.use_case.execute(request)
            spy_delete.assert_called_once()
            self.assertCountEqual(self.category_repo.items, [])
