import curses
import time
from functools import partial

from vert_tree.base import BaseTreeDisplay, TreeDisplayError
from vert_tree.common import Edge


class CursesDisplay(BaseTreeDisplay):
    def __init__(self, timeout=-1):
        self.timeout = timeout
        self.x = self.y = 0
        self.function = partial(curses.wrapper, self._display_curses_tree)

    def _init_display(self, tree):
        self.height = tree.vertical_length
        self.width = tree.total_width
        self.root_pos = tree.left_width
        try:
            self.pad = curses.newpad(self.height, self.width)
            self.pad.keypad(True)
            curses.curs_set(0)
        except:
            raise TreeDisplayError(
                "The curses lib cannot handle a tree so large! Height: {} width: {}".format(self.height, self.width)
            )
        # curses reads will block for only this time amount in millis
        self.pad.timeout(500)

    def _display_curses_tree(self, stdscr, root, edge_spacing):
        super(CursesDisplay, self)._base_display_tree(root, edge_spacing)
        _, win_width = stdscr.getmaxyx()
        # center pad on root element
        if win_width < self.width:
            self.x = self.root_pos - int(win_width / 2)
        time_end = self._get_end_time()
        while time.time() < time_end:
            win_height, win_width = stdscr.getmaxyx()
            self.pad.refresh(self.y, self.x, 0, 0, win_height - 1, win_width - 1)
            input_char = self._get_pad_char()
            if input_char == ord("q"):
                break
            elif input_char == curses.KEY_UP:
                self.y = max(self.y - 1, 0)
            elif input_char == curses.KEY_DOWN:
                self.y = min(self.y + 1, self.height - win_height)
            elif input_char == curses.KEY_RIGHT:
                self.x = min(self.x + 1, self.width - 2)
            elif input_char == curses.KEY_LEFT:
                self.x = max(self.x - 1, 0)

    def _get_pad_char(self):
        # used for simpler monkey patching in test
        return self.pad.getch()

    def _get_end_time(self):
        if self.timeout >= 0:
            return time.time() + self.timeout
        return float("inf")

    def _print_edges(self, level_edges, level, width, edge_spacing, lines_required):
        if not level_edges:
            return
        for edge in level_edges:
            curr_level = 0
            curr_pos = edge.parent_pos
            if edge.direction == "/":
                while curr_level < lines_required:
                    curr_pos -= edge.get_step_width(edge_spacing, curr_pos - edge.child_pos)
                    y = edge.distance_from_top + curr_level
                    self.pad.addch(y, curr_pos, edge.direction)
                    curr_level += 1
            else:
                while curr_level < lines_required:
                    curr_pos += edge.get_step_width(edge_spacing, edge.child_pos - curr_pos)
                    y = edge.distance_from_top + curr_level
                    self.pad.addch(y, curr_pos, edge.direction)
                    curr_level += 1

    def _print_vertices(self, level_verts, width):
        self._truncate_node_vals(level_verts)
        for vertex in level_verts:
            self.pad.addstr(vertex.distance_from_top, vertex.start, vertex.node.val)
