

from abc import ABC
from __seedwork.domain.repositories import (
    SearchParams as DefaultSearchParams,
    SearchResult as DefaultSearchResult,
    SearchableRepositoryInterface
)
from category.domain.entities import Category


class _SearchParams(DefaultSearchParams):
    pass


class _SearchResult(DefaultSearchResult):
    pass


class CategoryRepository(SearchableRepositoryInterface[Category, _SearchParams, _SearchResult], ABC):
    SearchParams = _SearchParams
    SearchResult = _SearchResult
