import unittest
import warnings

from district42 import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestAnyValidator(ValidatorTestCase):

  def test_it_validates_type(self):
    self.assertValidationPasses(42,       schema.any)
    self.assertValidationPasses(True,     schema.any)
    self.assertValidationPasses('banana', schema.any)
    self.assertValidationPasses([],       schema.any)
    self.assertValidationPasses({},       schema.any)

    self.assertValidationFails(None, schema.any)

  def test_it_validates_nullable(self):
    with warnings.catch_warnings():
      warnings.simplefilter('ignore')

      self.assertValidationPasses(None,     schema.any.nullable)
      self.assertValidationPasses(42,       schema.any.nullable)
      self.assertValidationPasses(True,     schema.any.nullable)
      self.assertValidationPasses('banana', schema.any.nullable)
      self.assertValidationPasses([],       schema.any.nullable)
      self.assertValidationPasses({},       schema.any.nullable)

      self.assertValidationFails(ValidatorTestCase, schema.any.nullable)
