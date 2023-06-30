from game import GoBoardGraph
from PySide6.QtCore import QPoint, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QBrush
from PySide6.QtWidgets import QGraphicsItem


'''
    GoBoard class
    This class is used to draw the board.
    It is a QGraphicsItem. It is added to the QGraphicsScene.
'''
class GoBoard(QGraphicsItem):
    cell_size = 30
    margin = 20
    size = 19

    def __init__(self, board: GoBoardGraph):
        super().__init__()
        self.board = board

    def boundingRect(self):
        return QRectF(0, 0, self.margin * 2 + self.cell_size * (self.size - 1), self.margin * 2 + self.cell_size * (self.size - 1))

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        self.__draw_wood_background(painter)
        self.__draw_star_points(painter)
        self.__draw_board(painter)

    def __draw_wood_background(self, painter: QPainter):
        rect = self.boundingRect()
        wood_color1 = QColor(240, 201, 155)
        wood_color2 = QColor(218, 180, 130)

        painter.setBrush(QBrush(wood_color1))
        painter.drawRect(rect)

        painter.setPen(QPen(wood_color2, 0.5, Qt.SolidLine,
                       Qt.RoundCap, Qt.RoundJoin))

        num_lines = 50
        for i in range(num_lines):
            x1 = rect.left() + (rect.width() / num_lines) * i
            y1 = rect.top()
            x2 = rect.left() + (rect.width() / num_lines) * (i + 1)
            y2 = rect.bottom()
            painter.drawLine(x1, y1, x2, y2)

        for i in range(num_lines):
            x1 = rect.left()
            y1 = rect.top() + (rect.height() / num_lines) * i
            x2 = rect.right()
            y2 = rect.top() + (rect.height() / num_lines) * (i + 1)
            painter.drawLine(x1, y1, x2, y2)

    def __draw_board(self, painter: QPainter):
        painter.setPen(QPen(QColor(0, 0, 0), 1))

        for i in range(self.size):
            start_point = QPoint(self.margin + i * self.cell_size, self.margin)
            end_point = QPoint(self.margin + i * self.cell_size,
                               self.margin + (self.size - 1) * self.cell_size)
            painter.drawLine(start_point, end_point)

            start_point = QPoint(self.margin, self.margin + i * self.cell_size)
            end_point = QPoint(self.margin + (self.size - 1) *
                               self.cell_size, self.margin + i * self.cell_size)
            painter.drawLine(start_point, end_point)

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    self.__draw_stone(painter, i, j, self.board[i][j])

    def __draw_star_points(self, painter: QPainter):
        star_point_radius = 4
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setBrush(QBrush(QColor(0, 0, 0)))

        star_points = [(3, 3), (3, 9), (3, 15),
                       (9, 3), (9, 9), (9, 15),
                       (15, 3), (15, 9), (15, 15)]

        for x, y in star_points:
            point = self.__calculate_point(x, y)
            painter.drawEllipse(point, star_point_radius, star_point_radius)

    def __calculate_point(self, x: int, y: int) -> QPoint:
        return QPoint(self.margin + x * self.cell_size, self.margin + y * self.cell_size)

    def __draw_stone(self, painter: QPainter, x: int, y: int, color: str):
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setBrush(QBrush(QColor(color)))
        painter.drawEllipse(self.__calculate_point(x, y), 10, 10)
