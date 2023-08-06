import unittest

from valeera import Formatter, Validator


class ValidatorTestCase(unittest.TestCase):

  def assertValidationPasses(self, actual, expected):
    validator = Validator(Formatter()).validate(actual, expected)
    return self.assertEqual(validator.errors(), [])

  def assertValidationFails(self, actual, expected):
    validator = Validator(Formatter()).validate(actual, expected)
    return self.assertNotEqual(validator.errors(), [])
