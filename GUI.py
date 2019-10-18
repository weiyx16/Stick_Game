# -*- coding: utf-8 -*-
import sys
from random import randrange
from game import Stick_game
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, 
    QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget)
from PyQt5.QtGui import (QIcon, QFont, QPainter, QBrush, QPen, QPalette, QPixmap)
from PyQt5.QtCore import QCoreApplication, Qt

class Digit():
    # Poverty
    # 1. show number
    # 2. possible to change certain line's color / type

    def __init__(self, loc = (0,0)):
        self.initUI(loc)
        self.num = {
            "0": [1,1,1,0,1,1,1],  #6
            "1": [0,0,1,0,0,1,0],  #2
            "2": [1,0,1,1,1,0,1],  #5
            "3": [1,0,1,1,0,1,1],  #5
            "4": [0,1,1,1,0,1,0],  #4
            "5": [1,1,0,1,0,1,1],  #5
            "6": [1,1,0,1,1,1,1],  #6
            "7": [1,0,1,0,0,1,0],  #3
            "8": [1,1,1,1,1,1,1],  #7
            "9": [1,1,1,1,0,1,1],  #6
            "None" : [0,0,0,0,0,0,0]
        }
        self.length = 10
        self.width = 4
        self.line_gap = 1
    def initUI(self, loc):
        """
        # number encoding order with:
        —— 1
        | 2 | 3
        —— 4
        | 5 | 6
        —— 7
        """
        self.line1 = QPainter(self)
        self.line1.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        self.line1.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        self.line1.drawRect(loc[0] + self.line_gap, loc[1], self.length, self.width)



class GUI(QWidget):
     
    def __init__(self):
        super(GUI, self).__init__()
         
        self.initUI()
        self.play = Stick_game(equation=[])
        self.question_database = None

    def initUI(self):
        
        QToolTip.setFont(QFont('SansSerif', 10))

        # question input
        title = QLabel(self)
        title.setText('题目输入：')
        title.move(50, 50)
        self.number1 = QLineEdit(self)
        self.number1.resize(75, 30)
        self.number1.move(150, 50)
        self.number1.textChanged[str].connect(self.number_1_update_display)
        self.num1_digit1 = []

        self.op1 = QComboBox(self)
        self.op1.move(250, 50)
        self.op1.addItems(['+', '-', 'x', '='])
        self.op1.currentIndexChanged[str].connect(self.op_1_update_display) # 条目发生改变，发射信号，传递条目内容
        self.op1.highlighted[str].connect(self.op_1_update_display)  # 在下拉列表中，鼠标移动到某个条目时发出信号，传递条目内容

        self.number2 = QLineEdit(self)
        self.number2.resize(75, 30)
        self.number2.move(320, 50)
        self.number2.textChanged[str].connect(self.number_2_update_display)

        self.op2 = QComboBox(self)
        self.op2.move(420, 50)
        self.op2.addItems(['+', '-', 'x', '='])
        self.op2.currentIndexChanged[str].connect(self.op_2_update_display) # 条目发生改变，发射信号，传递条目内容
        self.op2.highlighted[str].connect(self.op_1_update_display)  # 在下拉列表中，鼠标移动到某个条目时发出信号，传递条目内容

        self.number3 = QLineEdit(self)
        self.number3.resize(75, 30)
        self.number3.move(490, 50)
        self.number3.textChanged[str].connect(self.number_3_update_display)

        # Button 1: BFS Move One
        btn1 = QPushButton('一步法', self)
        btn1.clicked.connect(self.Solution_Step_One)
        btn1.resize(btn1.sizeHint())
        btn1.move(50, 300)
        
        # Button 2: BFS Move Two
        btn2 = QPushButton('两步法', self)
        btn2.clicked.connect(self.Solution_Step_Two)
        btn2.resize(btn2.sizeHint())
        btn2.move(200, 300)

        # Button 3: Question Generation 1 
        btn3 = QPushButton('生成一步问题', self)
        btn3.clicked.connect(self.Generation_Step_One)
        btn3.resize(btn3.sizeHint())
        btn3.move(350, 300)

        # Button 4: Question Generation 4
        btn4 = QPushButton('生成两步问题', self)
        btn4.clicked.connect(self.Generation_Step_Two)
        btn4.resize(btn4.sizeHint())
        btn4.move(525, 300)

        # Button 5: Answer Question from file
        btn5 = QPushButton('从库中选择问题', self)
        btn5.clicked.connect(self.Question_from_Database)
        btn5.resize(btn5.sizeHint())
        btn5.move(700, 50)

        # Button 6: Quit
        qbtn = QPushButton('退出', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(750, 300)
        
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('./ICON.png')))
        self.setPalette(palette1)
        # self.setAutoFillBackground(True)

        self.center()
        self.resize(900, 400)
        # self.setGeometry(300, 300, 900, 400) # 900*400
        self.setWindowTitle('Stick Game')
        self.setWindowIcon(QIcon('ICON.png'))       
     
        self.show()

    def center(self):
         
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
         
        reply = QMessageBox.question(self, '提示',
            "即将退出程序", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.Yes)
 
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 

    def op_1_update_display(self, op):
        if op == '+':
            pass
        elif op == '-':
            pass
        else:
            pass
    
    def op_2_update_display(self, op):
        if op == '+':
            pass
        elif op == '-':
            pass
        else:
            pass
    
    def number_1_update_display(self, number):
        if number:
            number = int(number)
            if number > 99:
                reply = QMessageBox.information(self, '提示', "请输入两位数字", QMessageBox.Ok, QMessageBox.Ok)
            elif number > 9:
                # number 2 digits
                pass
            else:
                pass
        else:
            # clear!
            print('None')
    
    def number_2_update_display(self, number):
        if number:
            number = int(number)
            if number > 99:
                reply = QMessageBox.information(self, '提示', "请输入两位数字", QMessageBox.Ok, QMessageBox.Ok)
            elif number > 9:
                # number 2 digits
                pass
            else:
                pass
        else:
            # clear!
            print('None')
    
    def number_3_update_display(self, number):
        if number:
            number = int(number)
            if number > 99:
                reply = QMessageBox.information(self, '提示', "请输入两位数字", QMessageBox.Ok, QMessageBox.Ok)
            elif number > 9:
                # number 2 digits
                pass
            else:
                pass
        else:
            # clear!
            print('None')

    def Solution_Step_One(self):
        ans = self.play.One_Stick()
        answer = self.solution_info(ans)
    
    def Solution_Step_Two(self):
        ans = self.play.Two_Stick()
        answer = self.solution_info(ans)

    def solution_info(self, ans):
        if not ans:
            QMessageBox.information(self, '抱歉', "当前条件下，此问题没有解法", QMessageBox.Ok, QMessageBox.Ok)
        else:
            if len(ans) > 1:
                QMessageBox.information(self, '提示', "已找到%d个解\n将随机选择答案显示" % len(ans), QMessageBox.Ok, QMessageBox.Ok)
                answer = ans[randrange(len(ans))]
            else:
                QMessageBox.information(self, '提示', "已找到1个解", QMessageBox.Ok, QMessageBox.Ok)
                answer = ans[0]
            return answer

    def Generation_Step_One(self):
        self.play.BFS_Move_One(is_generate=True)
    
    def Generation_Step_Two(self):
        self.play.BFS_Move_Two(is_generate=True)

    def Question_from_Database(self):
        if not self.question_database:
            with open('questions.txt', 'r') as f:
                self.question_database = f.readlines()
        self.question = self.question_database[randrange(len(self.question_database))]
        print(" >> Random pick question as " + self.question)
        def op_set(op, loc):
            index = loc.findText(op, Qt.MatchFixedString)
            if index >= 0:
                    loc.setCurrentIndex(index)
        # string to list
        self.question = self.question.replace('[','')
        self.question = self.question.replace(']','')
        self.question = self.question.replace("'",'')
        self.question = self.question.replace(" ",'')
        self.question = self.question.split(",")
        self.number1.setText(self.question[0])
        op_set(self.question[1], self.op1)
        self.number2.setText(self.question[2])
        op_set(self.question[3], self.op2)
        self.number3.setText(self.question[4])
        self.play.equation_update(self.question)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    
    sys.exit(app.exec_())