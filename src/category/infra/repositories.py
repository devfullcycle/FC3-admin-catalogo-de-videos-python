from typing import List
from category.domain.entities import Category
from category.domain.repositories import CategoryRepository
from __seedwork.domain.repositories import InMemorySearchableRepository


class CategoryInMemoryRepository(CategoryRepository, InMemorySearchableRepository):
    sortable_fields: List[str] = ["name", "created_at"]

    def _apply_filter(self, items: List[Category], filter_param: str = None) -> List[Category]:
        if filter_param:
            filter_obj = filter(
                lambda i: filter_param.lower() in i.name.lower(),
                items
            )
            return list(filter_obj)

        return items

    def _apply_sort(
        self,
        items:
        List[Category],
        sort: str = None,
        sort_dir:
        str = None
    ) -> List[Category]:
        return super()._apply_sort(items, sort, sort_dir) \
            if sort \
            else super()._apply_sort(items, "created_at", "desc")

# validação
#repositório - ordenação - created_at, filter - name
