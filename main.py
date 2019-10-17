# -*- coding: utf-8 -*-
import sys
from GUI import GUI
from game import Stick_game
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
     
    app = QApplication(sys.argv)
    ex = GUI()
    play = Stick_game(equation=[])
    sys.exit(app.exec_()) 