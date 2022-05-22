# pylint: disable=unexpected-keyword-arg
from typing import Optional
import unittest

from datetime import datetime
from category.application.dto import CategoryOutput, CategoryOutputMapper
from category.domain.entities import Category


class TestCategoryOutputUnit(unittest.TestCase):

    def test_fields(self):
        self.assertEqual(CategoryOutput.__annotations__, {
            'id': str,
            'name': str,
            'description': Optional[str],
            'is_active': bool,
            'created_at': datetime
        })


class CategoryOutputChild(CategoryOutput):  # pylint: disable=too-few-public-methods
    pass


class TestCategoryOutputMapperUnit(unittest.TestCase):

    def test_to_output_from_child(self):
        mapper = CategoryOutputMapper\
            .from_child(CategoryOutputChild)
        self.assertIsInstance(mapper, CategoryOutputMapper)
        self.assertTrue(
            issubclass(
                mapper.output_child,
                CategoryOutputChild
            )
        )

    def test_to_output_without_child(self):
        mapper = CategoryOutputMapper.without_child()
        self.assertIsInstance(mapper, CategoryOutputMapper)
        self.assertTrue(
            issubclass(
                mapper.output_child,
                CategoryOutput
            )
        )

    def test_to_output(self):
        created_at = datetime.now()
        entity = Category(
            name='test',
            description='some description',
            is_active=True,
            created_at=created_at
        )
        output = CategoryOutputMapper.without_child().to_output(
            entity)  # pylint: disable=duplicate-code
        self.assertEqual(output, CategoryOutput(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at
        ))

        output = CategoryOutputMapper.from_child(
            CategoryOutputChild).to_output(entity)
        self.assertEqual(output, CategoryOutputChild(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at
        ))
