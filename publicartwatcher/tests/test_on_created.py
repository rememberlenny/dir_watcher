from unittest import TestCase

import publicartwatcher

class TestOnCreated(TestCase):
    def test_is_string(self):
        s = publicart_watcher.joke()
        self.assertTrue(isinstance(s, basestring))