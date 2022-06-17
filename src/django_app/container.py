from dependency_injector import containers, providers
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
    GetCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)


class Container(containers.DeclarativeContainer):

    repository_category_in_memory = providers.Singleton(
        CategoryInMemoryRepository)

    use_case_category_create_category = providers.Singleton(
        CreateCategoryUseCase, category_repo=repository_category_in_memory
    )

    use_case_category_list_categories = providers.Singleton(
        ListCategoriesUseCase, category_repo=repository_category_in_memory
    )

    use_case_category_get_category = providers.Singleton(
        GetCategoryUseCase, category_repo=repository_category_in_memory
    )

    use_case_category_update_category = providers.Singleton(
        UpdateCategoryUseCase, category_repo=repository_category_in_memory
    )

    use_case_category_delete_category = providers.Singleton(
        DeleteCategoryUseCase, category_repo=repository_category_in_memory
    )
