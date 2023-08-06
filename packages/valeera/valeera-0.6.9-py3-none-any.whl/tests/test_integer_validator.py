import unittest
import warnings

from district42 import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestIntegerValidator(ValidatorTestCase):

  def test_it_validates_type(self):
    self.assertValidationPasses(-1, schema.integer)
    self.assertValidationPasses(0,  schema.integer)
    self.assertValidationPasses(1,  schema.integer)

    self.assertValidationFails(None,  schema.integer)
    self.assertValidationFails(False, schema.integer)
    self.assertValidationFails(3.14,  schema.integer)
    self.assertValidationFails('0',   schema.integer)
    self.assertValidationFails([],    schema.integer)
    self.assertValidationFails({},    schema.integer)

  def test_it_validates_value(self):
    self.assertValidationPasses(42,  schema.integer(42))
    self.assertValidationPasses(-42, schema.integer(-42))
    self.assertValidationPasses(0,   schema.integer.zero)

    self.assertValidationFails(None, schema.integer(0))
    self.assertValidationFails(42,   schema.integer(-42))
    self.assertValidationFails(-42,  schema.integer(42))
    self.assertValidationFails(3.14, schema.integer(3))
    self.assertValidationFails('0',  schema.integer.zero)

  def test_it_validates_min_value(self):
    self.assertValidationPasses(0, schema.integer.min(0))
    self.assertValidationPasses(1, schema.integer.min(0))
    
    self.assertValidationFails(-1, schema.integer.min(0))

  def test_it_validates_max_value(self):
    self.assertValidationPasses(0, schema.integer.max(1))
    self.assertValidationPasses(1, schema.integer.max(1))
    
    self.assertValidationFails(2, schema.integer.max(1))

  def test_it_validates_multiple(self):
    self.assertValidationPasses(-25, schema.integer.multiple(5))
    self.assertValidationPasses(0,   schema.integer.multiple(5))
    self.assertValidationPasses(25,  schema.integer.multiple(5))

    self.assertValidationFails(1, schema.integer.multiple(5))

  def test_it_validates_nullable(self):
    with warnings.catch_warnings():
      warnings.simplefilter('ignore')
      self.assertValidationPasses(None, schema.integer.nullable)
      self.assertValidationPasses(None, schema.integer(42).nullable)

      self.assertValidationFails(False, schema.integer.nullable)
      self.assertValidationFails('',    schema.integer.nullable)
      self.assertValidationFails([],    schema.integer.nullable)
      self.assertValidationFails({},    schema.integer.nullable)
