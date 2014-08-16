from unittest import TestCase

from ..util import maybe, singleton


class TestUtil(TestCase):
    def test_maybe_none_case(self):
        result = maybe(1, lambda x: x + 2, None)
        self.assertEqual(result, 1)

    def test_maybe_some_case(self):
        result = maybe(1, lambda x: x + 2, 3)
        self.assertEqual(result, 5)

    def test_singleton(self):
        result = singleton(5)
        self.assertEqual(result, [5])

    def test_singleton_none(self):
        result = singleton(None)
        self.assertEqual(result, [None])
