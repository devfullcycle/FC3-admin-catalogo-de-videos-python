import unittest
from core.__seedwork.application.use_cases import UseCase


class TestUseCases(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            UseCase()
        self.assertEqual(assert_error.exception.args[0],
                         "Can't instantiate abstract class UseCase with abstract " +
                         "method execute"
                         )
