import unittest

from util import captured_output, create_tree_1
from vert_tree import CursesDisplay, TerminalDisplay


class TestBase(unittest.TestCase):
    def setUp(self):
        self.term_display = TerminalDisplay(False)
        self.curses_display = CursesDisplay()

    def test_none_root(self):
        root = None
        with captured_output() as (stdout, stderr):
            self.term_display.display_vert_tree(root, 4)
            output = stdout.getvalue().splitlines()
        assert output[0] == "Error: no tree to display"
        with captured_output() as (stdout, stderr):
            self.curses_display.display_vert_tree(root, 4)
            output = stdout.getvalue().splitlines()
        assert output[0] == "Error: no tree to display"

    def test_non_power_2(self):
        root = create_tree_1()
        with captured_output() as (stdout, stderr):
            self.term_display.display_vert_tree(root, 3)
            output = stdout.getvalue().splitlines()
        assert output[0] == "Error: edge spacing must be a power of two"
        with captured_output() as (stdout, stderr):
            self.curses_display.display_vert_tree(root, 3)
            output = stdout.getvalue().splitlines()
        assert output[0] == "Error: edge spacing must be a power of two"
