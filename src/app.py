import sys
from PySide6 import QtWidgets


class BoardWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.board = [[0 for _ in range(4)] for _ in range(4)]

        self.table = QtWidgets.QTableWidget(4, 4)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()

        for i in range(4):
            self.table.setColumnWidth(i, 50)
            self.table.setRowHeight(i, 50)

        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.table.cellClicked.connect(self.cell_clicked)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.update_board()

    def update_board(self):
        for i in range(4):
            for j in range(4):
                self.table.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(self.board[i][j])))

    def cell_clicked(self, row, column):
        self.board[row][column] = 1 - self.board[row][column]
        self.update_board()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = BoardWidget()
    widget.resize(300, 300)
    widget.show()

    sys.exit(app.exec())
