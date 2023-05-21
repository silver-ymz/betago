import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QColorConstants
from setting import load_word


class BoardWidget(QtWidgets.QWidget):
    def __init__(self, init_table: list[list[int]] = None):
        super().__init__()

        self.board_size = 16
        self.cell_size = 50
        if init_table is None:
            self.board = [[0 for _ in range(self.board_size)]
                          for _ in range(self.board_size)]
        else:
            assert len(init_table) == self.board_size
            assert all(len(i) == self.board_size for i in init_table)
            self.board = init_table

        self.table = QtWidgets.QTableWidget(self.board_size, self.board_size)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()

        for i in range(self.board_size):
            self.table.setColumnWidth(i, self.cell_size)
            self.table.setRowHeight(i, self.cell_size)

        for i in range(self.board_size):
            for j in range(self.board_size):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem())

        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.table.cellClicked.connect(self.cell_clicked)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.update_board()

    def update_board(self):
        for i in range(16):
            for j in range(16):
                if self.board[i][j] == 0:
                    self.table.item(i, j).setBackground(QColorConstants.White)
                else:
                    self.table.item(i, j).setBackground(QColorConstants.Black)

    @QtCore.Slot(int, int)
    def cell_clicked(self, row: int, column: int):
        self.board[row][column] = 1 - self.board[row][column]
        self.update_board()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    word = load_word('settings/1.txt')

    widget = BoardWidget(word)
    widget.resize(1000, 1000)
    widget.show()

    sys.exit(app.exec())
