import abc
from collections import deque

import six
from vert_tree.common import Edge, Tree, Vertex


class TreeDisplayError(Exception):
    pass


@six.add_metaclass(abc.ABCMeta)
class BaseTreeDisplay:
    @abc.abstractmethod
    def _init_display(self, tree):
        pass

    @abc.abstractmethod
    def _print_vertices(self, level_verts, width):
        pass

    @abc.abstractmethod
    def _print_edges(self, level_edges, level, width, edge_spacing):
        pass

    def display_vert_tree(self, root, edge_spacing=1):
        # we don't want to take down the user program if something goes wrong
        try:
            self.function(root, edge_spacing)
        except TreeDisplayError as cde:
            print(cde)

    def _base_display_tree(self, root, edge_spacing=1):
        if root is None:
            raise TreeDisplayError("Error: no tree to display")
        # ensure edge spacing is a power of 2
        if not ((edge_spacing != 0) and (edge_spacing & (edge_spacing - 1) == 0)):
            raise TreeDisplayError("Error: edge spacing must be a power of two")
        tree = Tree(root, edge_spacing)
        self._init_display(tree)
        current_level, next_level = deque(), deque()
        distance_from_top, level_verts, level_edges = 0, [], []
        current_level.append(Vertex(root, distance_from_top, tree.left_width, tree.depth - 1, tree.total_width))
        while current_level:
            cur = current_level.popleft()
            level_verts.append(cur)
            next_edge_len = Edge.get_edge_length(cur.levels_below, edge_spacing)
            child_dis = distance_from_top + next_edge_len + 1
            if cur.node.left:
                child_pos = cur.position_from_left - pow(2, cur.levels_below)
                next_level.append(Vertex(cur.node.left, child_dis, child_pos, cur.levels_below - 1, tree.total_width))
                level_edges.append(Edge(distance_from_top + 1, cur.position_from_left, child_pos, "/"))
            if cur.node.right:
                child_pos = cur.position_from_left + pow(2, cur.levels_below)
                next_level.append(Vertex(cur.node.right, child_dis, child_pos, cur.levels_below - 1, tree.total_width))
                level_edges.append(Edge(distance_from_top + 1, cur.position_from_left, child_pos, chr(92)))
            if not current_level:
                self._print_vertices(level_verts, tree.total_width)
                self._print_edges(level_edges, cur.levels_below, tree.total_width, edge_spacing, next_edge_len)
                distance_from_top += next_edge_len + 1
                level_edges, level_verts = [], []
                current_level = next_level
                next_level = deque()

    def _truncate_node_vals(self, level_verts):
        for i in range(len(level_verts) - 1):
            left = level_verts[i]
            right = level_verts[i + 1]
            while left.does_overlap(right):
                longer = left.longer_val_node(right)
                longer.trim_val()
