from unittest import TestCase

from publicart_watcher.command_line import main


class TestCmd(TestCase):
    def test_basic(self):
        main()