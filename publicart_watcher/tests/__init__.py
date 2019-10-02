from unittest import TestCase

import publicart_watcher


class TestMain(TestCase):
    def test_is_working(self):
        s = publicart_watcher.confirm_working()
        self.assertTrue(isinstance(s, basestring))