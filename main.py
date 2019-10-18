# -*- coding: utf-8 -*-
import sys
from GUI import GUI
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
     
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_()) 