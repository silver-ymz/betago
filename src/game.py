from typing import Tuple
from graph import GoBoardGraph
from PySide6.QtWidgets import QMessageBox


'''
    GoGame class
    This class represents a game of Go.
    It is used to play moves and check for game over.
'''
class GoGame:
    size = 19

    def __init__(self):
        self.player = "black"
        self.game_over = False
        self.board = GoBoardGraph(self.size)
        self.player_pass = {"black": False, "white": False}
        self.anti = False

    def play_move(self, x: int, y: int) -> bool:
        position = (x, y)
        if not self.__is_on_board(x, y):
            return False

        if self.board[x][y] is not None:
            return False

        if self.__causes_self_capture(position):
            QMessageBox.critical(None, "Illegal move",
                                 "Self capture is not allowed.")
            return False

        self.board[x][y] = self.player

        captured_stones = self.__capture_stones(position)
        for captured_position in captured_stones:
            self.board.set_color(captured_position, None)

        self.player_pass[self.player] = False
        self.__switch_player()
        return True

    def pass_turn(self):
        self.player_pass[self.player] = True
        self.__switch_player()

        if self.__check_game_end():
            self.game_over = True
            self.__score_game()

    def opponent(self) -> str:
        return "white" if self.player == "black" else "black"
    
    def __switch_player(self):
        self.player = self.opponent()

    def __check_game_end(self):
        return all(self.player_pass.values())

    def __causes_self_capture(self, position: Tuple[int, int]) -> bool:
        temp_board = GoBoardGraph(self.size)
        temp_board.graph = self.board.graph.copy()
        temp_board.node_colors = self.board.node_colors.copy()

        temp_board.set_color(position, self.player)
        group = temp_board.get_connected_component(position)
        liberties = self.__get_liberties(group, temp_board)

        if len(liberties) != 0:
            self.anti = False
            return False

        if self.anti:
            return True

        # Check if the move is an anti-killing move.
        opponent = self.opponent()
        for neighbor in temp_board.get_neighbors(position):
            if temp_board.get_color(neighbor) == opponent:
                opponent_group = temp_board.get_connected_component(neighbor)
                opponent_liberties = self.__get_liberties(
                    opponent_group, temp_board)

                # If the opponent doesn't have liberty, it's an anti-killing move.
                if len(opponent_liberties) == 0:
                    self.anti = True
                    return False

        return True

    def __capture_stones(self, position) -> list[Tuple[int, int]]:
        captured_stones = []
        opponent = self.opponent()

        for neighbor in self.board.get_neighbors(position):
            if self.board.get_color(neighbor) == opponent:
                group = self.board.get_connected_component(neighbor)
                liberties = self.__get_liberties(group, self.board)
                if len(liberties) == 0:
                    captured_stones.extend(group)

        return captured_stones

    def __is_on_board(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def __get_liberties(self, group, board: GoBoardGraph) -> set[Tuple[int, int]]:
        liberties = set()
        for position in group:
            for neighbor in board.get_neighbors(position):
                if board.get_color(neighbor) is None:
                    liberties.add(neighbor)
        return liberties

    def __score_game(self):
        final_message = ""

        territory = {"black": 0, "white": 0}
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None:
                    surrounded_color = self.__check_surrounded_color(i, j)
                    if surrounded_color is not None:
                        territory[surrounded_color] += 1
                else:
                    territory[self.board[i][j]] += 1

        final_message += "Game Over\n"
        final_message += "Black's score: {}\n".format(territory["black"])
        final_message += "White's score: {}\n".format(territory["white"])

        if territory["black"] > territory["white"]:
            final_message += "Black wins\n"
        elif territory["black"] < territory["white"]:
            final_message += "White wins\n"
        else:
            final_message += "The game is a draw\n"

        QMessageBox.information(None, "Game over", final_message)

    def __check_surrounded_color(self, x, y):
        visited = set()
        stack = [(x, y)]
        surrounded_color = None

        while stack:
            current_x, current_y = stack.pop()
            visited.add((current_x, current_y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor_x, neighbor_y = current_x + dx, current_y + dy

                if 0 <= neighbor_x < self.size and 0 <= neighbor_y < self.size:
                    neighbor_color = self.board[neighbor_x][neighbor_y]

                    if neighbor_color is None and (neighbor_x, neighbor_y) not in visited:
                        stack.append((neighbor_x, neighbor_y))
                    elif neighbor_color is not None:
                        if surrounded_color is None:
                            surrounded_color = neighbor_color
                        elif surrounded_color != neighbor_color:
                            return None

        return surrounded_color
