import sys
from game import GoGame
from window import GoGUI
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    go_game = GoGame()
    go_gui = GoGUI(go_game)
    go_gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
