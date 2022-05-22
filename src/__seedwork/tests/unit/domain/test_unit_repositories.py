# pylint: disable=unexpected-keyword-arg,protected-access

from dataclasses import dataclass
from typing import List, Optional
import unittest
from __seedwork.domain.entities import Entity
from __seedwork.domain.repositories import (
    ET,
    Filter,
    InMemoryRepository,
    InMemorySearchableRepository,
    RepositoryInterface,
    SearchParams,
    SearchResult,
    SearchableRepositoryInterface
)
from __seedwork.domain.exceptions import NotFoundException
from __seedwork.domain.value_objects import UniqueEntityId


class TestRepositoryInterface(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            RepositoryInterface()
        self.assertEqual(assert_error.exception.args[0],
                         "Can't instantiate abstract class RepositoryInterface with abstract " +
                         "methods delete, find_all, find_by_id, insert, update"
                         )


@dataclass(frozen=True, kw_only=True, slots=True)
class StubEntity(Entity):
    name: str
    price: float


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    pass


class TestInMemoryRepository(unittest.TestCase):

    repo: StubInMemoryRepository

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()

    def test_items_prop_is_empty_on_init(self):
        self.assertEqual(self.repo.items, [])

    def test_insert(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)
        self.assertEqual(self.repo.items[0], entity)

    def test_throw_not_found_exception_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('fake id')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake id'")

        unique_entity_id = UniqueEntityId(
            'af46842e-027d-4c91-b259-3a3642144ba4')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID 'af46842e-027d-4c91-b259-3a3642144ba4'"
        )

    def test_find_by_id(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)

        entity_found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity_found, entity)

        entity_found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(entity_found, entity)

    def test_find_all(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)

        items = self.repo.find_all()
        self.assertListEqual(items, [entity])

    def test_throw_not_found_exception_in_update(self):
        entity = StubEntity(name='test', price=5)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.update(entity)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'")

    def test_update(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)

        entity_updated = StubEntity(
            unique_entity_id=entity.unique_entity_id, name='updated', price=1)
        self.repo.update(entity_updated)

        self.assertEqual(entity_updated, self.repo.items[0])

    def test_throw_not_found_exception_in_delete(self):
        entity = StubEntity(name='test', price=5)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity.id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'")

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity.unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'")

    def test_delete(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)

        self.repo.delete(entity.id)
        self.assertListEqual(self.repo.items, [])

        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)

        self.repo.delete(entity.unique_entity_id)
        self.assertListEqual(self.repo.items, [])


class TestSearchableRepositoryInterface(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            SearchableRepositoryInterface()
        self.assertEqual(
            "Can't instantiate abstract class SearchableRepositoryInterface with abstract " +
            "methods delete, find_all, find_by_id, insert, search, update",
            assert_error.exception.args[0]
        )

    def test_sortable_fields_prop(self):
        self.assertEqual(SearchableRepositoryInterface.sortable_fields, [])


class TestSearchParams(unittest.TestCase):

    def test_props_annotations(self):
        self.assertEqual(SearchParams.__annotations__, {
            'page': Optional[int],
            'per_page': Optional[int],
            'sort': Optional[str],
            'sort_dir': Optional[str],
            'filter': Optional[Filter]
        })

    def test_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.page, 1)

        arrange = [
            {'page': None, 'expected': 1},
            {'page': "", 'expected': 1},
            {'page': "fake", 'expected': 1},
            {'page': 0, 'expected': 1},
            {'page': -1, 'expected': 1},
            {'page': "0", 'expected': 1},
            {'page': "-1", 'expected': 1},
            {'page': 5.5, 'expected': 5},
            {'page': True, 'expected': 1},
            {'page': False, 'expected': 1},
            {'page': {}, 'expected': 1},
            {'page': 1, 'expected': 1},
            {'page': 2, 'expected': 2},
        ]

        for i in arrange:
            params = SearchParams(page=i['page'])
            self.assertEqual(params.page, i['expected'])

    def test_per_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.per_page, 15)

        arrange = [
            {'per_page': None, 'expected': 15},
            {'per_page': "", 'expected': 15},
            {'per_page': "fake", 'expected': 15},
            {'per_page': 0, 'expected': 15},
            {'per_page': -1, 'expected': 15},
            {'per_page': "0", 'expected': 15},
            {'per_page': "-1", 'expected': 15},
            {'per_page': 5.5, 'expected': 5},
            {'per_page': True, 'expected': 1},
            {'per_page': False, 'expected': 15},
            {'per_page': {}, 'expected': 15},
            {'per_page': 1, 'expected': 1},
            {'per_page': 2, 'expected': 2},
        ]

        for i in arrange:
            params = SearchParams(per_page=i['per_page'])
            self.assertEqual(params.per_page, i['expected'], i)

    def test_sort_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort)

        arrange = [
            {'sort': None, 'expected': None},
            {'sort': "", 'expected': None},
            {'sort': "fake", 'expected': 'fake'},
            {'sort': 0, 'expected': '0'},
            {'sort': -1, 'expected': '-1'},
            {'sort': "0", 'expected': '0'},
            {'sort': "-1", 'expected': '-1'},
            {'sort': 5.5, 'expected': '5.5'},
            {'sort': True, 'expected': 'True'},
            {'sort': False, 'expected': 'False'},
            {'sort': {}, 'expected': '{}'},
        ]

        for i in arrange:
            params = SearchParams(sort=i['sort'])
            self.assertEqual(params.sort, i['expected'], i)

    def test_sort_dir_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort=None)
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort="")
        self.assertIsNone(params.sort_dir)

        arrange = [
            {'sort_dir': None, 'expected': 'asc'},
            {'sort_dir': "", 'expected': 'asc'},
            {'sort_dir': "fake", 'expected': 'asc'},
            {'sort_dir': 0, 'expected': 'asc'},
            {'sort_dir': {}, 'expected': 'asc'},
            {'sort_dir': 'asc', 'expected': 'asc'},
            {'sort_dir': 'ASC', 'expected': 'asc'},
            {'sort_dir': 'desc', 'expected': 'desc'},
            {'sort_dir': 'DESC', 'expected': 'desc'},
        ]

        for i in arrange:
            params = SearchParams(sort='name', sort_dir=i['sort_dir'])
            self.assertEqual(params.sort_dir, i['expected'], i)

    def test_filter_prop(self):
        params = SearchParams()
        self.assertIsNone(params.filter)

        arrange = [
            {'filter': None, 'expected': None},
            {'filter': "", 'expected': None},
            {'filter': "fake", 'expected': 'fake'},
            {'filter': 0, 'expected': '0'},
            {'filter': -1, 'expected': '-1'},
            {'filter': "0", 'expected': '0'},
            {'filter': "-1", 'expected': '-1'},
            {'filter': 5.5, 'expected': '5.5'},
            {'filter': True, 'expected': 'True'},
            {'filter': False, 'expected': 'False'},
            {'filter': {}, 'expected': '{}'},
        ]

        for i in arrange:
            params = SearchParams(filter=i['filter'])
            self.assertEqual(params.filter, i['expected'], i)


class TestSearchResult(unittest.TestCase):

    def test_props_annotations(self):
        self.assertEqual(SearchResult.__annotations__, {
            'items': List[ET],
            'total': int,
            'current_page': int,
            'per_page': int,
            'last_page': int,
            'sort': Optional[str],
            'sort_dir': Optional[str],
            'filter': Optional[Filter]
        })

    def test_constructor(self):
        entity = StubEntity(name='fake', price=5)
        result = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=2
        )

        self.assertDictEqual(result.to_dict(), {
            'items': [entity, entity],
            'total': 4,
            'current_page': 1,
            'per_page': 2,
            'last_page': 2,
            'sort': None,
            'sort_dir': None,
            'filter': None
        })

        result = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='test'
        )

        self.assertDictEqual(result.to_dict(), {
            'items': [entity, entity],
            'total': 4,
            'current_page': 1,
            'per_page': 2,
            'last_page': 2,
            'sort': 'name',
            'sort_dir': 'asc',
            'filter': 'test'
        })

    def test_when_per_page_is_greater_than_total(self):
        result = SearchResult(
            items=[],
            total=4,
            current_page=1,
            per_page=15,
        )
        self.assertEqual(result.last_page, 1)

    def test_when_per_page_is_less_than_total_and_they_are_not_multiples(self):
        result = SearchResult(
            items=[],
            total=101,
            current_page=1,
            per_page=20,
        )
        self.assertEqual(result.last_page, 6)


class StubInMemorySearchableRepository(InMemorySearchableRepository[StubEntity, str]):
    sortable_fields: List[str] = ['name']

    def _apply_filter(self, items: List[StubEntity], filter_param: str | None) -> List[StubEntity]:
        if filter_param:
            filter_obj = filter(lambda i: filter_param.lower() in i.name.lower()
                                or filter_param == str(i.price), items)
            return list(filter_obj)
        return items


class TestInMemorySearchableRepository(unittest.TestCase):

    repo: StubInMemorySearchableRepository

    def setUp(self) -> None:
        self.repo = StubInMemorySearchableRepository()

    def test__apply_filter(self):
        items = [StubEntity(name='test', price=5)]
        # pylint: disable=protected-access
        result = self.repo._apply_filter(items, None)
        self.assertEqual(items, result)

        items = [
            StubEntity(name='test', price=5),
            StubEntity(name='TEST', price=5),
            StubEntity(name='fake', price=0),
        ]

        # pylint: disable=protected-access
        result = self.repo._apply_filter(items, 'TEST')
        self.assertEqual([items[0], items[1]], result)

        # pylint: disable=protected-access
        result = self.repo._apply_filter(items, '5')
        self.assertEqual([items[0], items[1]], result)

    def test__apply_sort(self):
        items = [
            StubEntity(name='b', price=1),
            StubEntity(name='a', price=0),
            StubEntity(name='c', price=2),
        ]

        result = self.repo._apply_sort(items, 'price', 'asc')
        self.assertEqual(items, result)

        result = self.repo._apply_sort(items, 'name', 'asc')
        self.assertEqual([items[1], items[0], items[2]], result)

        result = self.repo._apply_sort(items, 'name', 'desc')
        self.assertEqual([items[2], items[0], items[1]], result)

        self.repo.sortable_fields.append('price')
        result = self.repo._apply_sort(items, 'price', 'asc')
        self.assertEqual([items[1], items[0], items[2]], result)

        result = self.repo._apply_sort(items, 'price', 'desc')
        self.assertEqual([items[2], items[0], items[1]], result)

    def test__apply_paginate(self):
        items = [
            StubEntity(name='a', price=1),
            StubEntity(name='b', price=1),
            StubEntity(name='c', price=1),
            StubEntity(name='d', price=1),
            StubEntity(name='e', price=1),
        ]

        result = self.repo._apply_paginate(items, 1, 2)
        self.assertEqual([items[0], items[1]], result)

        result = self.repo._apply_paginate(items, 2, 2)
        self.assertEqual([items[2], items[3]], result)

        result = self.repo._apply_paginate(items, 3, 2)
        self.assertEqual([items[4]], result)

        result = self.repo._apply_paginate(items, 4, 2)
        self.assertEqual([], result)

    def test_search_when_params_is_empty(self):
        entity = StubEntity(name='a', price=1)
        items = [entity] * 16
        self.repo.items = items

        result = self.repo.search(SearchParams())
        self.assertEqual(result, SearchResult(
            items=[entity] * 15,
            total=16,
            current_page=1,
            per_page=15,
            sort=None,
            sort_dir=None,
            filter=None
        ))

    def test_search_applying_filter_and_paginate(self):
        items = [
            StubEntity(name='test', price=1),
            StubEntity(name='a', price=1),
            StubEntity(name='TEST', price=1),
            StubEntity(name='TeSt', price=1),
        ]
        self.repo.items = items

        result = self.repo.search(SearchParams(
            page=1, per_page=2, filter='TEST'
        ))
        self.assertEqual(result, SearchResult(
            items=[items[0], items[2]],
            total=3,
            current_page=1,
            per_page=2,
            sort=None,
            sort_dir=None,
            filter='TEST'
        ))

        result = self.repo.search(SearchParams(
            page=2, per_page=2, filter='TEST'
        ))
        self.assertEqual(result, SearchResult(
            items=[items[3]],
            total=3,
            current_page=2,
            per_page=2,
            sort=None,
            sort_dir=None,
            filter='TEST'
        ))

        result = self.repo.search(SearchParams(
            page=3, per_page=2, filter='TEST'
        ))
        self.assertEqual(result, SearchResult(
            items=[],
            total=3,
            current_page=3,
            per_page=2,
            sort=None,
            sort_dir=None,
            filter='TEST'
        ))

    def test_search_applying_sort_and_paginate(self):
        items = [
            StubEntity(name='b', price=1),
            StubEntity(name='a', price=1),
            StubEntity(name='d', price=1),
            StubEntity(name='e', price=1),
            StubEntity(name='c', price=1),
        ]
        self.repo.items = items

        arrange_by_asc = [
            {
                'input': SearchParams(
                    page=1, per_page=2, sort='name'
                ),
                'output': SearchResult(
                    items=[items[1], items[0]],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort='name',
                    sort_dir='asc',
                    filter=None
                )
            },
            {
                'input': SearchParams(
                    page=2, per_page=2, sort='name'
                ),
                'output': SearchResult(
                    items=[items[4], items[2]],
                    total=5,
                    current_page=2,
                    per_page=2,
                    sort='name',
                    sort_dir='asc',
                    filter=None
                )
            },
            {
                'input': SearchParams(
                    page=3, per_page=2, sort='name'
                ),
                'output': SearchResult(
                    items=[items[3]],
                    total=5,
                    current_page=3,
                    per_page=2,
                    sort='name',
                    sort_dir='asc',
                    filter=None
                )
            }
        ]

        for index, item in enumerate(arrange_by_asc):
            result = self.repo.search(item['input'])
            self.assertEqual(
                result,
                item['output'],
                f"The output using sort_dir asc on index {index} is different"
            )

        arrange_by_desc = [
            {
                'input': SearchParams(
                    page=1, per_page=2, sort='name', sort_dir='desc'
                ),
                'output': SearchResult(
                    items=[items[3], items[2]],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None
                )
            },
            {
                'input': SearchParams(
                    page=2, per_page=2, sort='name', sort_dir='desc'
                ),
                'output': SearchResult(
                    items=[items[4], items[0]],
                    total=5,
                    current_page=2,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None
                )
            },
            {
                'input': SearchParams(
                    page=3, per_page=2, sort='name', sort_dir='desc'
                ),
                'output': SearchResult(
                    items=[items[1]],
                    total=5,
                    current_page=3,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None
                )
            }
        ]

        for index, item in enumerate(arrange_by_desc):
            result = self.repo.search(item['input'])
            self.assertEqual(
                result,
                item['output'],
                f"The output using sort_dir desc on index {index} is different"
            )

    def test_search_applying_filter_and_sort_and_paginate(self):
        items = [
            StubEntity(name='test', price=1),
            StubEntity(name='a', price=1),
            StubEntity(name='TEST', price=1),
            StubEntity(name='e', price=1),
            StubEntity(name='TeSt', price=1),
        ]
        self.repo.items = items

        result = self.repo.search(SearchParams(
            page=1,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))

        self.assertEqual(result, SearchResult(
            items=[items[2], items[4]],
            total=3,
            current_page=1,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))

        result = self.repo.search(SearchParams(
            page=2,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))

        self.assertEqual(result, SearchResult(
            items=[items[0]],
            total=3,
            current_page=2,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))
