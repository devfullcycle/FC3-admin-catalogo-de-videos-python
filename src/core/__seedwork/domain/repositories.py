

from abc import ABC
import abc
from dataclasses import dataclass, field
import math
from typing import Any, Generic, List, Optional, TypeVar
from __seedwork.domain.value_objects import UniqueEntityId
from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import NotFoundException

ET = TypeVar('ET', bound=Entity)


class RepositoryInterface(Generic[ET], ABC):

    @abc.abstractmethod
    def insert(self, entity: ET) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_all(self) -> List[ET]:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, entity: ET) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, entity_id: str | UniqueEntityId) -> None:
        raise NotImplementedError()


Input = TypeVar('Input')
Output = TypeVar('Output')


class SearchableRepositoryInterface(Generic[ET, Input, Output], RepositoryInterface[ET], ABC):

    sortable_fields: List[str] = []

    @abc.abstractmethod
    def search(self, input_params: Input) -> Output:
        raise NotImplementedError()


Filter = TypeVar('Filter', str, Any)


@dataclass(slots=True, kw_only=True)
class SearchParams(Generic[Filter]):
    page: Optional[int] = 1
    per_page: Optional[int] = 15
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None

    def __post_init__(self):
        self._normalize_page()
        self._normalize_per_page()
        self._normalize_sort()
        self._normalize_sort_dir()
        self._normalize_filter()

    def _normalize_page(self):
        page = self._convert_to_int(self.page)
        if page <= 0:
            page = self._get_dataclass_field('page').default
        self.page = page

    def _normalize_per_page(self):
        per_page = self._convert_to_int(self.per_page)
        if per_page < 1:
            per_page = self._get_dataclass_field('per_page').default
        self.per_page = per_page

    def _normalize_sort(self):
        self.sort = None if self.sort == "" or self.sort is None \
            else str(self.sort)

    def _normalize_sort_dir(self):
        if not self.sort:
            self.sort_dir = None
            return

        sort_dir = str(self.sort_dir).lower()
        self.sort_dir = 'asc' if sort_dir not in ['asc', 'desc'] else sort_dir

    def _normalize_filter(self):
        self.filter = None if self.filter == "" or self.filter is None \
            else str(self.filter)

    def _convert_to_int(self, value: Any, default=0) -> int:  # pylint: disable=no-self-use
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def _get_dataclass_field(self, field_name):  # pylint: disable=no-self-use
        return SearchParams.__dataclass_fields__[field_name]  # pylint: disable=no-member


@dataclass(slots=True, kw_only=True, frozen=True)
class SearchResult(Generic[ET, Filter]):  # pylint: disable=too-many-instance-attributes
    items: List[ET]
    total: int
    current_page: int
    per_page: int
    last_page: int = field(init=False)
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None

    def __post_init__(self):
        object.__setattr__(
            self,
            'last_page',
            math.ceil(self.total / self.per_page)
        )

    def to_dict(self):
        return {
            'items': self.items,
            'total': self.total,
            'current_page': self.current_page,
            'per_page': self.per_page,
            'last_page': self.last_page,
            'sort': self.sort,
            'sort_dir': self.sort_dir,
            'filter': self.filter,
        }


@dataclass(slots=True)
class InMemoryRepository(RepositoryInterface[ET], ABC):
    items: List[ET] = field(default_factory=lambda: [])

    def insert(self, entity: ET) -> None:
        self.items.append(entity)

    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        id_str = str(entity_id)
        return self._get(id_str)

    def find_all(self) -> List[ET]:
        return self.items

    def update(self, entity: ET) -> None:
        entity_found = self._get(entity.id)
        index = self.items.index(entity_found)
        self.items[index] = entity

    def delete(self, entity_id: str | UniqueEntityId) -> None:
        id_str = str(entity_id)
        entity_found = self._get(id_str)
        self.items.remove(entity_found)

    def _get(self, entity_id: str) -> ET:
        entity = next(filter(lambda i: i.id == entity_id, self.items), None)
        if not entity:
            raise NotFoundException(f"Entity not found using ID '{entity_id}'")
        return entity


class InMemorySearchableRepository(
    Generic[ET, Filter],
    InMemoryRepository[ET],
    SearchableRepositoryInterface[
        ET,
        SearchParams[Filter],
        SearchResult[ET, Filter]
    ],
    ABC
):
    def search(self, input_params: SearchParams[Filter]) -> SearchResult[ET, Filter]:
        items_filtered = self._apply_filter(self.items, input_params.filter)
        items_sorted = self._apply_sort(
            items_filtered, input_params.sort, input_params.sort_dir)
        items_paginated = self._apply_paginate(
            items_sorted, input_params.page, input_params.per_page)

        return SearchResult(
            items=items_paginated,
            total=len(items_filtered),
            current_page=input_params.page,
            per_page=input_params.per_page,
            sort=input_params.sort,
            sort_dir=input_params.sort_dir,
            filter=input_params.filter
        )

    @abc.abstractmethod
    def _apply_filter(self, items: List[ET], filter_param: Filter | None) -> List[ET]:
        raise NotImplementedError()

    def _apply_sort(self, items: List[ET], sort: str | None, sort_dir: str | None) -> List[ET]:
        if sort and sort in self.sortable_fields:
            is_reverse = sort_dir == 'desc'
            return sorted(items, key=lambda item: getattr(item, sort), reverse=is_reverse)
        return items

    def _apply_paginate(self, items: List[ET], page: int, per_page: int) -> List[ET]:  # pylint: disable=no-self-use
        start = (page - 1) * per_page
        limit = start + per_page
        return items[slice(start, limit)]
