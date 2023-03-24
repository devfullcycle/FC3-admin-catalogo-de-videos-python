
# pylint:  disable=unexpected-keyword-arg
from datetime import datetime
from dataclasses import dataclass, field
from faker import Faker
from typing import Any, Callable, Generic, List, TypeVar
from core.__seedwork.domain.value_objects import UniqueEntityId
from .entities import Category

T = TypeVar('T')

PropOrFactory = T | Callable[[int], T]


@dataclass
class CategoryFakerBuilder(Generic[T]):
    count_objs: int = 1

    __unique_entity_id: PropOrFactory[UniqueEntityId] = field(
        default=None, init=False
    )
    __name: PropOrFactory[str] = field(
        default=lambda self, index: Faker().name(), init=False
    )
    __description: PropOrFactory[str | None] = field(
        default=lambda self, index: Faker().sentence(), init=False
    )
    __is_active: bool = field(default=lambda self, index: True, init=False)
    __created_at: PropOrFactory[datetime] = field(
        default=None, init=False
    )

    @staticmethod
    def a_category() -> 'CategoryFakerBuilder[Category]':
        return CategoryFakerBuilder()

    @staticmethod
    def the_categories(count: int) -> 'CategoryFakerBuilder[List[Category]]':
        return CategoryFakerBuilder(count)

    @staticmethod
    def a_movie():
        return CategoryFakerBuilder()

    # @staticmethod
    # def a_deactivate_category():
    #     return CategoryFakerBuilder()

    def with_unique_entity_id(self, value: PropOrFactory[UniqueEntityId]):
        self.__unique_entity_id = value
        return self

    def with_name(self, value: PropOrFactory[str]):
        self.__name = value
        return self

    def with_description(self, value: PropOrFactory[str | None]):
        self.__description = value
        return self

    def activate(self):
        self.__is_active = True
        return self

    def deactivate(self):
        self.__is_active = False
        return self

    def with_created_at(self, value: PropOrFactory[datetime]):
        self.__created_at = value
        return self

    def with_invalid_name_none(self):
        self.__name = None
        return self

    def with_invalid_name_empty(self):
        self.__name = ""
        return self

    def with_invalid_name_not_a_string(self, value: Any = None):
        self.__name = value if value is not None else 123
        return self

    def with_invalid_name_too_long(self, value: str = None):
        self.__name = value if value is not None else ''.join(
            Faker().random_letters(length=256)
        )
        return self

    def with_invalid_description_not_a_string(self, value: Any = None):
        self.__description = value if value is not None else 123
        return self

    def with_invalid_is_active_none(self):
        self.__is_active = None
        return self

    def with_invalid_is_active_empty(self):
        self.__is_active = ""
        return self

    def with_invalid_is_active_not_a_boolean(self, value: Any = None):
        self.__is_active = value if value is not None else 123
        return self

    def build(self) -> T:
        categories = list(
            map(
                lambda index: Category(**{
                    **({
                        'unique_entity_id': self.__call_factory(self.__unique_entity_id, index),
                    } if self.__unique_entity_id is not None else {}),
                    'name': self.__call_factory(self.__name, index),
                    'description': self.__call_factory(self.__description, index),
                    'is_active': self.__call_factory(self.__is_active, index),
                    **({
                        'created_at': self.__call_factory(self.__created_at, index),
                    } if self.__created_at is not None else {}),
                }),
                list(range(self.count_objs))
            )
        )
        return categories if self.count_objs > 1 else categories[0]

    @property
    def unique_entity_id(self) -> UniqueEntityId:
        value = self.__call_factory(self.__unique_entity_id, 0)
        if value is None:
            raise Exception(
                'Prop unique_entity_id not have a factory, use "with methods"'
            )
        return value

    @property
    def name(self) -> str:
        return self.__call_factory(self.__name, 0)

    @property
    def description(self) -> str | None:
        return self.__call_factory(self.__description, 0)

    @property
    def is_active(self) -> bool:
        return self.__call_factory(self.__is_active, 0)

    @property
    def created_at(self) -> datetime:
        value = self.__call_factory(self.__created_at, 0)
        if value is None:
            raise Exception(
                'Prop created_at not have a factory, use "with methods"'
            )
        return value

    def __call_factory(self, value: PropOrFactory[Any], index: int) -> Any:
        return value(index) if callable(value) else value
# funcao -> valor ou valor
