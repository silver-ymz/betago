from board import GoBoard
from game import GoGame
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout, QLabel, QMessageBox


'''
    GoGUI class
    This class is the main window of the game.
    It contains the board and the pass button.
    It also handles the mouse click event.
'''
class GoGUI(QMainWindow):
    def __init__(self, go_game: GoGame):
        super().__init__()
        self.go_game = go_game
        self.__init_timer()
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle("Go Game")
        self.setGeometry(0, 0, 800, 600)
        self.setFixedSize(800, 600)

        self.board = GoBoard(self.go_game.board)
        self.board.setPos(0, 0)

        self.scene = QGraphicsScene()
        self.scene.addItem(self.board)

        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 600, 600)
        self.view.setFixedSize(600, 600)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.text_label = QLabel(self)
        self.text_label.setGeometry(0, 0, 100, 50)
        self.text_label.move(650, 100)
        self.text_label.setText("Black's turn")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("QLabel { font-size: 20px; }")

        self.time_label = QLabel(self)
        self.time_label.setGeometry(0, 0, 200, 50)
        self.time_label.move(600, 200)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("QLabel { font-size: 15px; }")
        self.__update_time_label()

        self.button = QPushButton("Pass", self)
        self.button.setGeometry(0, 0, 100, 50)
        self.button.clicked.connect(self.pass_turn)
        self.button.move(650, 400)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.text_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def __init_timer(self):
        timer_black = QTimer(self)
        timer_black.timeout.connect(self.on_timeout)
        timer_white = QTimer(self)
        timer_white.timeout.connect(self.on_timeout)
        self.timer = {"black": timer_black, "white": timer_white}
        self.remain_time = {"black": 3600 * 1000, "white": 3600 * 1000}
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_time_remaining)
        self.update_timer.setInterval(1000)  # 1 second
        self.update_timer.start()
        self.timer["black"].start(self.remain_time["black"])

    @Slot()
    def mousePressEvent(self, event):
        if self.go_game.game_over:
            return

        if event.button() == Qt.MouseButton.LeftButton:
            x, y = event.position().x(), event.position().y()
            idx_x = round(
                (x - self.board.margin - self.board.cell_size / 2) / self.board.cell_size)
            idx_y = round(
                (y - self.board.margin - self.board.cell_size / 2) / self.board.cell_size)
            if self.go_game.play_move(idx_x, idx_y):
                self.board.update()
                self.text_label.setText(self.go_game.player.capitalize() + "'s turn")
                self.__update_player_time(is_pass=False)

    @Slot()
    def pass_turn(self):
        if self.go_game.game_over:
            return
        
        self.go_game.pass_turn()

        if self.go_game.game_over:
            self.text_label.setText("Game Over")
        else:
            self.text_label.setText(self.go_game.player.capitalize() + "'s turn")
            self.__update_player_time(is_pass=True)

    @Slot()
    def on_timeout(self):
        QMessageBox.critical(self, "Timeout", "Time is up!")
        self.timer[self.go_game.player].setInterval(0)
        self.pass_turn()

    @Slot()
    def update_time_remaining(self):
        if self.go_game.game_over:
            return

        self.__update_time_label()
        self.update_timer.setInterval(1000)
        self.update_timer.start()

    def __update_player_time(self, is_pass: bool):
        self.update_timer.stop()
        self.remain_time[self.go_game.opponent()] = self.timer[self.go_game.opponent()].remainingTime() + (60 * 1000 if not is_pass else 0)
        self.timer[self.go_game.player].start(self.remain_time[self.go_game.player])
        self.timer[self.go_game.opponent()].stop()
        self.update_time_remaining()
        self.update_timer.start()

    def __update_time_label(self):
        if self.timer["black"].isActive():
            self.time_label.setText("Black time " + self.__format_time(self.timer["black"].remainingTime()) +
                                "\nWhite time " + self.__format_time(self.remain_time["white"]))
        else:
            self.time_label.setText("Black time " + self.__format_time(self.remain_time["black"]) +
                                "\nWhite time " + self.__format_time(self.timer["white"].remainingTime()))
        
    def __format_time(self, time: int):
        if time < 0:
            return "00:00"
        else:
            return str(time // 60000).zfill(2) + ":" + str((time // 1000) % 60).zfill(2)