
from datetime import datetime
import unittest
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities_faker_builder import CategoryFakerBuilder


class TestCategoryFakeBuilder(unittest.TestCase):

    def test_unique_entity_id_prop_throw_exception_when_is_none(self):
        with self.assertRaises(Exception) as assert_exception:
            faker = CategoryFakerBuilder.a_category()
            faker.unique_entity_id
        self.assertEqual(
            str(assert_exception.exception),
            'Prop unique_entity_id not have a factory, use "with methods"'
        )

    def test_unique_entity_id_prop(self):
        faker = CategoryFakerBuilder.a_category()
        unique_entity_id = UniqueEntityId()
        this = faker.with_unique_entity_id(unique_entity_id)

        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertEqual(faker.unique_entity_id, unique_entity_id)

    def test_invalid_cases_for_name_prop(self):
        faker = CategoryFakerBuilder.a_category()
        this = faker.with_invalid_name_none()
        self.assertIsInstance(this, CategoryFakerBuilder)

        name_value = this.name
        self.assertIsNone(name_value)

        name_value = faker.with_invalid_name_empty().name
        self.assertEqual(name_value, "")

        name_value = faker.with_invalid_name_not_a_string().name
        self.assertEqual(name_value, 123)

        name_value = faker.with_invalid_name_not_a_string(10).name
        self.assertEqual(name_value, 10)

        name_value = faker.with_invalid_name_too_long().name
        self.assertEqual(len(name_value), 256)

    def test_name_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertIsInstance(faker.name, str)

        this = faker.with_name('name test')
        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertEqual(faker.name, 'name test')

    def test_description_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertIsInstance(faker.description, str)

        this = faker.with_description('description test')
        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertEqual(faker.description, 'description test')

    def test_is_active_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertTrue(faker.is_active)

        this = faker.deactivate()
        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertFalse(faker.is_active)

        this = faker.activate()
        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertTrue(faker.is_active)

    def test_created_at_prop_throw_exception_when_is_none(self):
        with self.assertRaises(Exception) as assert_exception:
            faker = CategoryFakerBuilder.a_category()
            faker.created_at
        self.assertEqual(
            str(assert_exception.exception),
            'Prop created_at not have a factory, use "with methods"'
        )

    def test_created_at_prop(self):
        faker = CategoryFakerBuilder.a_category()
        date = datetime.now()
        this = faker.with_created_at(date)

        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertEqual(faker.created_at, date)

    def test_build_a_category(self):
        faker = CategoryFakerBuilder.a_category()
        category = faker.build()

        self.assert_category_prop_types(category)

        unique_entity_id = UniqueEntityId()
        date = datetime.now()
        builder = faker.with_unique_entity_id(unique_entity_id)\
            .with_name('name test')\
            .with_description('description test')\
            .deactivate()\
            .with_created_at(date)

        category = builder.build()
        self.assertIsNotNone(category)
        self.assert_category(category, unique_entity_id, date)

        category = builder.activate().build()
        self.assertTrue(category.is_active)

    def test_build_the_categories(self):
        faker = CategoryFakerBuilder.the_categories(2)
        categories = faker.build()

        self.assertIsNotNone(categories)
        self.assertIsInstance(categories, list)
        self.assertEqual(len(categories), 2)

        for category in categories:
            self.assert_category_prop_types(category)

        unique_entity_id = UniqueEntityId()
        date = datetime.now()
        builder = faker.with_unique_entity_id(unique_entity_id)\
            .with_name('name test')\
            .with_description('description test')\
            .deactivate()\
            .with_created_at(date)

        categories = builder.build()

        for category in categories:
            self.assert_category(category, unique_entity_id, date)

        categories = builder.activate().build()
        for category in categories:
            self.assertTrue(category.is_active)

    def assert_category_prop_types(self, category):
        self.assertIsNotNone(category)
        self.assertIsInstance(category.unique_entity_id, UniqueEntityId)
        self.assertIsInstance(category.name, str)
        self.assertIsInstance(category.description, str)
        self.assertIsInstance(category.is_active, bool)
        self.assertTrue(category.is_active)
        self.assertIsInstance(category.created_at, datetime)

    def assert_category(self, category, unique_entity_id, created_at):
        self.assertEqual(category.unique_entity_id, unique_entity_id)
        self.assertEqual(category.name, 'name test')
        self.assertEqual(category.description, 'description test')
        self.assertFalse(category.is_active)
        self.assertEqual(category.created_at, created_at)
