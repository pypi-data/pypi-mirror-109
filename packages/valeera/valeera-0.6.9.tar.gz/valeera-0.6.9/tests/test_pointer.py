import unittest

from valeera.pointer import Pointer


class TestPointer(unittest.TestCase):

  def setUp(self):
    self.dictionary = {
      'result': {
        'total': 2,
        'items': [
          {'id': 1},
          {'id': 2}
        ]
      }
    }

  def test_it_returns_path(self):
    pointer = Pointer(self.dictionary)
    self.assertEqual(pointer.path(), '#')

    pointer = Pointer(self.dictionary, ['result'])
    self.assertEqual(pointer.path(), '#.result')

    pointer = Pointer(self.dictionary, ['result', 'total'])
    self.assertEqual(pointer.path(), '#.result.total')

    pointer = Pointer(self.dictionary, ['result', 'items'])
    self.assertEqual(pointer.path(), '#.result.items')

    pointer = Pointer(self.dictionary, ['result', 'items', 0])
    self.assertEqual(pointer.path(), '#.result.items[0]')

    pointer = Pointer(self.dictionary, ['result', 'items', 0, 'id'])
    self.assertEqual(pointer.path(), '#.result.items[0].id')

  def test_it_checks_value_existence(self):
    pointer = Pointer(self.dictionary)
    self.assertTrue(pointer.has_value())

    pointer = Pointer(self.dictionary, ['result'])
    self.assertTrue(pointer.has_value())

    pointer = Pointer(self.dictionary, ['result', 'total'])
    self.assertTrue(pointer.has_value())

    pointer = Pointer(self.dictionary, ['result', 'items'])
    self.assertTrue(pointer.has_value())

    pointer = Pointer(self.dictionary, ['result', 'items', 0])
    self.assertTrue(pointer.has_value())

    pointer = Pointer(self.dictionary, ['result', 'items', 2])
    self.assertFalse(pointer.has_value())

    pointer = Pointer(self.dictionary, ['result', 'items', 0, 'id'])
    self.assertTrue(pointer.has_value())

    pointer = Pointer(self.dictionary, ['banana', 'items', 0, 'id'])
    self.assertFalse(pointer.has_value())

    pointer = Pointer(self.dictionary, ['result', 'items', 0, 'title'])
    self.assertFalse(pointer.has_value())

  def test_it_returns_value(self):
    pointer = Pointer(self.dictionary)
    self.assertEqual(pointer.value(), self.dictionary)

    pointer = Pointer(self.dictionary, ['result'])
    self.assertEqual(pointer.value(), self.dictionary['result'])

    pointer = Pointer(self.dictionary, ['result', 'total'])
    self.assertEqual(pointer.value(), self.dictionary['result']['total'])

    pointer = Pointer(self.dictionary, ['result', 'items'])
    self.assertEqual(pointer.value(), self.dictionary['result']['items'])

    pointer = Pointer(self.dictionary, ['result', 'items', 0])
    self.assertEqual(pointer.value(), self.dictionary['result']['items'][0])

    pointer = Pointer(self.dictionary, ['result', 'items', 0, 'id'])
    self.assertEqual(pointer.value(), self.dictionary['result']['items'][0]['id'])

  def test_it_moves(self):
    origin_pointer = Pointer(self.dictionary)
    pointer = origin_pointer.move('result').move('items').move(0).move('id')
    
    self.assertEqual(pointer.path(), '#.result.items[0].id')
    self.assertEqual(pointer.value(), self.dictionary['result']['items'][0]['id'])

    self.assertEqual(origin_pointer.path(), '#')
    self.assertEqual(origin_pointer.value(), self.dictionary)
