
import unittest

from category.domain.validators import CategoryValidator, CategoryValidatorFactory


class TestCategoryValidatorUnit(unittest.TestCase):

    validator: CategoryValidator

    def setUp(self) -> None:
        self.validator = CategoryValidatorFactory.create()
        return super().setUp()

    def test_invalidation_cases_for_name_field(self):

        invalid_data = [
            {'data': None, 'expected': 'This field is required.'},
            {'data': {}, 'expected': 'This field is required.'},
            {'data': {'name': None}, 'expected': 'This field may not be null.'},
            {'data': {'name': ''}, 'expected': 'This field may not be blank.'},
            {'data': {'name': 5}, 'expected': 'Not a valid string.'},
            {'data': {'name': 'a'*256},
                'expected': 'Ensure this field has no more than 255 characters.'},
        ]

        for i in invalid_data:
            is_valid = self.validator.validate(i['data'])
            self.assertFalse(is_valid)
            self.assertIn('name', self.validator.errors)
            self.assertListEqual(
                self.validator.errors['name'],
                [i['expected']],
                f'Expected: {i["expected"]}, actual: {self.validator.errors["name"][0]}'
            )

    def test_invalidation_cases_for_description_field(self):
        is_valid = self.validator.validate({'description': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['description'], [
                             'Not a valid string.'])

    def test_invalidation_cases_for_is_active_field(self):
        is_valid = self.validator.validate({'is_active': None})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], [
                             'This field may not be null.'])

        is_valid = self.validator.validate({'is_active': 0})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], [
                             'Must be a valid boolean.'])

        is_valid = self.validator.validate({'is_active': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], [
                             'Must be a valid boolean.'])

    def test_invalidation_cases_for_created_at_field(self):
        is_valid = self.validator.validate({'created_at': None})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['created_at'], [
                             'This field may not be null.'])

        is_valid = self.validator.validate({'created_at': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['created_at'], [
                             'Datetime has wrong format. Use one of these formats instead: ' +
                             'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'])

    def test_validate_cases(self):

        valid_data = [
            {'name': 'Movie'},
            {'name': 'Movie', 'description': None},
            {'name': 'Movie', 'description': ''},
            {'name': 'Movie', 'description': 'some description'},
            {'name': 'Movie', 'is_active': True},
            {'name': 'Movie', 'is_active': False},
            {'name': 'Movie', 'description': 'some description', 'is_active': True},
        ]

        for i in valid_data:
            is_valid = self.validator.validate(i)
            self.assertTrue(is_valid)
