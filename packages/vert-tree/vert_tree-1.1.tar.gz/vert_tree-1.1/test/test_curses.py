import curses
import unittest

from util import *
from vert_tree import CursesDisplay


class TestCurses(unittest.TestCase):
    def setUp(self):
        self.display = CursesDisplay(0)

    def test_tree_1(self):
        root = create_tree_1()
        self.display.display_vert_tree(root, 4)
        assert self.display.pad.instr(0, 4, 1) == b"a"
        assert self.display.pad.instr(2, 2, 1) == b"b"
        assert self.display.pad.instr(2, 6, 1) == b"c"
        assert self.display.pad.instr(1, 3, 1) == b"/"
        assert self.display.pad.instr(1, 5, 1) == b"\\"

    def test_tree_2(self):
        root = create_tree_2()
        self.display.display_vert_tree(root, 4)
        assert self.display.pad.instr(0, 8, 1) == b"a"
        assert self.display.pad.instr(2, 4, 1) == b"b"
        assert self.display.pad.instr(2, 12, 1) == b"c"
        assert self.display.pad.instr(4, 2, 1) == b"d"
        assert self.display.pad.instr(4, 6, 1) == b"e"
        assert self.display.pad.instr(4, 10, 1) == b"f"
        assert self.display.pad.instr(4, 14, 1) == b"g"
        assert self.display.pad.instr(1, 6, 1) == b"/"
        assert self.display.pad.instr(1, 10, 1) == b"\\"
        assert self.display.pad.instr(3, 3, 1) == b"/"
        assert self.display.pad.instr(3, 5, 1) == b"\\"
        assert self.display.pad.instr(3, 11, 1) == b"/"
        assert self.display.pad.instr(3, 13, 1) == b"\\"

    def test_tree_3(self):
        root = create_tree_3()
        self.display.display_vert_tree(root, 4)
        assert self.display.pad.instr(0, 16, 1) == b"a"
        assert self.display.pad.instr(2, 8, 1) == b"b"
        assert self.display.pad.instr(2, 24, 1) == b"c"
        assert self.display.pad.instr(4, 4, 1) == b"d"
        assert self.display.pad.instr(4, 12, 1) == b"e"
        assert self.display.pad.instr(4, 20, 1) == b"f"
        assert self.display.pad.instr(4, 28, 1) == b"g"
        assert self.display.pad.instr(6, 2, 1) == b"h"
        assert self.display.pad.instr(1, 12, 1) == b"/"
        assert self.display.pad.instr(1, 20, 1) == b"\\"
        assert self.display.pad.instr(3, 6, 1) == b"/"
        assert self.display.pad.instr(3, 10, 1) == b"\\"
        assert self.display.pad.instr(3, 22, 1) == b"/"
        assert self.display.pad.instr(3, 26, 1) == b"\\"
        assert self.display.pad.instr(5, 3, 1) == b"/"

    def test_tree_scroll(self):
        # display needs to remain up long enough to register our right arrows
        temp_display = CursesDisplay(1)
        root = create_tree_3()
        temp_display.display_vert_tree(root, 4)
        assert curses.getsyx()[1] == 3
        temp_display._get_pad_char = lambda: curses.KEY_RIGHT
        temp_display.display_vert_tree(root, 4)
        assert curses.getsyx()[1] == 0

    def test_root_centering(self):
        root = create_tree_4()
        self.display.display_vert_tree(root, 4)
        assert self.display.x != 0

    def test_too_large_tree(self):
        root = generate_random_tree(20)
        with captured_output() as (stdout, stderr):
            self.display.display_vert_tree(root)
            output = stdout.getvalue().splitlines()
        assert output[0][:45] == "The curses lib cannot handle a tree so large!"

    def test_random_trees(self):
        root = generate_random_tree(10)
        for _ in range(20):
            self.display.display_vert_tree(root)
