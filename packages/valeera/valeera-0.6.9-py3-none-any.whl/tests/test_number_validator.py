import unittest
import warnings

from district42 import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestNumberValidator(ValidatorTestCase):

  def setUp(self):
    warnings.simplefilter('ignore')

  def test_it_validates_type(self):
    self.assertValidationPasses(-3.14, schema.number)
    self.assertValidationPasses(-1,    schema.number)
    self.assertValidationPasses(0,     schema.number)
    self.assertValidationPasses(1,     schema.number)
    self.assertValidationPasses(3.14,  schema.number)

    self.assertValidationFails(None,  schema.number)
    self.assertValidationFails(False, schema.number)
    self.assertValidationFails('0',   schema.number)
    self.assertValidationFails([],    schema.number)
    self.assertValidationFails({},    schema.number)

  def test_it_validates_value(self):
    self.assertValidationPasses(42,    schema.number(42))
    self.assertValidationPasses(-42,   schema.number(-42))
    self.assertValidationPasses(3.14,  schema.number(3.14))
    self.assertValidationPasses(-3.14, schema.number(-3.14))
    self.assertValidationPasses(0,     schema.number.zero)
    self.assertValidationPasses(0.0,   schema.number.zero)

    self.assertValidationFails(None, schema.number(0))
    self.assertValidationFails(42,   schema.number(-42))
    self.assertValidationFails(-42,  schema.number(42))
    self.assertValidationFails(3.14, schema.number(3))
    self.assertValidationFails(3,    schema.number(3.14))
    self.assertValidationFails('0',  schema.number.zero)

  def test_it_validates_min_value(self):
    self.assertValidationPasses(0,    schema.number.min(0))
    self.assertValidationPasses(1,    schema.number.min(0))
    self.assertValidationPasses(3.14, schema.number.min(3.14))
    self.assertValidationPasses(3.15, schema.number.min(3.14))
    
    self.assertValidationFails(-1,    schema.number.min(0))
    self.assertValidationFails(-3.14, schema.number.min(-3.13))

  def test_it_validates_max_value(self):
    self.assertValidationPasses(0,    schema.number.max(1))
    self.assertValidationPasses(1,    schema.number.max(1))
    self.assertValidationPasses(3.13, schema.number.max(3.14))
    self.assertValidationPasses(3.14, schema.number.max(3.14))
    
    self.assertValidationFails(2,    schema.number.max(1))
    self.assertValidationFails(3.15, schema.number.max(3.14))

  def test_it_validates_range_restriction(self):
    self.assertValidationPasses(0,  schema.number.between(0, 1))
    self.assertValidationPasses(1,  schema.number.between(0, 1))
    self.assertValidationPasses(1,  schema.number.positive)
    self.assertValidationPasses(0,  schema.number.non_positive)
    self.assertValidationPasses(-1, schema.number.non_positive)
    self.assertValidationPasses(-1, schema.number.negative)
    self.assertValidationPasses(0,  schema.number.non_negative)
    self.assertValidationPasses(1,  schema.number.non_negative)
    self.assertValidationPasses(0,  schema.number.unsigned)
    self.assertValidationPasses(1,  schema.number.unsigned)

    self.assertValidationFails(-1, schema.number.between(0, 1))
    self.assertValidationFails(2,  schema.number.between(0, 1))
    self.assertValidationFails(0,  schema.number.positive)
    self.assertValidationFails(-1, schema.number.positive)
    self.assertValidationFails(1,  schema.number.non_positive)
    self.assertValidationFails(0,  schema.number.negative)
    self.assertValidationFails(1,  schema.number.negative)
    self.assertValidationFails(-1, schema.number.non_negative)
    self.assertValidationFails(-1, schema.number.unsigned)

  def test_it_validates_multiple(self):
    self.assertValidationPasses(-25, schema.number.multiple(5))
    self.assertValidationPasses(0,   schema.number.multiple(5))
    self.assertValidationPasses(25,  schema.number.multiple(5))

    self.assertValidationFails(1, schema.number.multiple(5))

  def test_it_validates_nullable(self):
    self.assertValidationPasses(None, schema.number.nullable)
    self.assertValidationPasses(None, schema.number(42).nullable)
    self.assertValidationPasses(None, schema.number(3.14).nullable)

    self.assertValidationFails(False, schema.number.nullable)
    self.assertValidationFails('',    schema.number.nullable)
    self.assertValidationFails([],    schema.number.nullable)
    self.assertValidationFails({},    schema.number.nullable)
