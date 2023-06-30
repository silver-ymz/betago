from collections import defaultdict
from typing import Tuple
import networkx as nx


'''
    GoBoardGraph class
    This class represents a Go board as a graph.
    It is used to find connected components.
'''
class GoBoardGraph:
    def __init__(self, size: int):
        self.size = size
        self.graph = nx.Graph()
        self.node_colors = defaultdict(lambda: None)

        # Add nodes and edges to the graph
        for x in range(size):
            for y in range(size):
                self.graph.add_node((x, y))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    neighbor_x, neighbor_y = x + dx, y + dy
                    if 0 <= neighbor_x < size and 0 <= neighbor_y < size:
                        self.graph.add_edge((x, y), (neighbor_x, neighbor_y))

    def get_neighbors(self, position: Tuple[int, int]) -> list[Tuple[int, int]]:
        return list(self.graph.neighbors(position))

    def get_color(self, position: Tuple[int, int]) -> str:
        return self.node_colors[position]

    def set_color(self, position: Tuple[int, int], color: str):
        self.node_colors[position] = color

    def get_connected_component(self, position: Tuple[int, int]) -> set[Tuple[int, int]]:
        return nx.node_connected_component(self.graph.subgraph(
            [node for node, color in self.node_colors.items() if color == self.node_colors[position]]),
            position)

    def __getitem__(self, i):
        if not 0 <= i < self.size:
            raise IndexError("Index out of bounds")
        return GoBoardGraphRowAccessor(self, i)

    def __setitem__(self, i, value):
        raise TypeError("GoBoardGraph does not support item assignment")


'''
    GoBoardGraphRowAccessor class
    This class is used to access a row of a GoBoardGraph.
    It is used to access the board like this:
        board = GoBoardGraph(9)
        board[0][0] = "black"
        print(board[0][0]) # "black"

    This is equivalent to:
        board = GoBoardGraph(9)
        board.set_color((0, 0), "black")
        print(board.get_color((0, 0))) # "black"
'''
class GoBoardGraphRowAccessor:
    def __init__(self, go_board_graph, row):
        self.go_board_graph = go_board_graph
        self.row = row

    def __getitem__(self, j):
        if not 0 <= j < self.go_board_graph.size:
            raise IndexError("Index out of bounds")
        return self.go_board_graph.get_color((self.row, j))

    def __setitem__(self, j, value):
        if not 0 <= j < self.go_board_graph.size:
            raise IndexError("Index out of bounds")
        self.go_board_graph.set_color((self.row, j), value)
