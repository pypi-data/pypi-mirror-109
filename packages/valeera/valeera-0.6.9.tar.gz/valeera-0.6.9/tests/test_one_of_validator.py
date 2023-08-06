import unittest
import warnings

from district42 import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestOneOfValidator(ValidatorTestCase):

  def test_it_validates_options(self):
    option1 = schema.object({'id': schema.integer})
    option2 = schema.object({'id': schema.string.numeric})
    option3 = schema.object({'deleted': schema.boolean})

    self.assertValidationPasses({'id': 42},         schema.one_of(option1, option2))
    self.assertValidationPasses({'id': '42'},       schema.one_of(option1, option2))
    self.assertValidationPasses({'id': 42},         schema.one_of(option1, option3))
    self.assertValidationPasses({'deleted': False}, schema.one_of(option1, option3))

    self.assertValidationFails({'id': None},                 schema.one_of(option1, option2))
    self.assertValidationFails({'id': 42, 'deleted': False}, schema.one_of(option1, option3))

  def test_it_validates_options_with_nullable_type(self):
    option1 = schema.object({'id': schema.integer})
    option2 = schema.object({'id': schema.string.numeric})
    option3 = schema.null

    self.assertValidationPasses(None,         schema.one_of(option1, option2, option3))
    self.assertValidationPasses({'id': 42},   schema.one_of(option1, option2, option3))
    self.assertValidationPasses({'id': '42'}, schema.one_of(option1, option2, option3))

    self.assertValidationPasses(None, schema.one_of(option1, option2, schema.null).nullable)

    self.assertValidationFails(False, schema.one_of(option1, option2, option3))
    self.assertValidationFails(0,     schema.one_of(option1, option2, option3))
    self.assertValidationFails('',    schema.one_of(option1, option2, option3))
    self.assertValidationFails([],    schema.one_of(option1, option2, option3))
    self.assertValidationFails({},    schema.one_of(option1, option2, option3))

  def test_it_validates_nullable(self):
    with warnings.catch_warnings():
      warnings.simplefilter('ignore')

      option1 = schema.object({'id': schema.integer})
      option2 = schema.object({'id': schema.string.numeric})

      self.assertValidationPasses(None,         schema.one_of(option1, option2).nullable)
      self.assertValidationPasses({'id': 42},   schema.one_of(option1, option2).nullable)
      self.assertValidationPasses({'id': '42'}, schema.one_of(option1, option2).nullable)

      self.assertValidationFails(False, schema.one_of(option1, option2).nullable)
      self.assertValidationFails(0,     schema.one_of(option1, option2).nullable)
      self.assertValidationFails('',    schema.one_of(option1, option2).nullable)
      self.assertValidationFails([],    schema.one_of(option1, option2).nullable)
      self.assertValidationFails({},    schema.one_of(option1, option2).nullable)
