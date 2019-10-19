# -*- coding: utf-8 -*-
import sys
from random import randrange
from game import Stick_game
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, 
    QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget, QListWidget)
from PyQt5.QtGui import (QIcon, QFont, QPainter, QBrush, QPen, QPalette, QPixmap)
from PyQt5.QtCore import QCoreApplication, Qt

class Question_GUI(QWidget):
    def __init__(self, parent=None, ans=None, questions=None):
        super(Question_GUI, self).__init__(parent)
        self.initUI(ans, questions)
    
    def initUI(self, ans, questions):
        self.setGeometry(300, 300, 200, 200) # 100*300
        QToolTip.setFont(QFont('SansSerif', 15))
        self.setWindowTitle('Question Generation')
        self.setWindowIcon(QIcon('./image/ICON.png'))       
        
        self.answer_show = QListWidget(self)
        self.answer_show.resize(200, 20)
        self.answer_show.addItem(self.list2str(ans))  # list 2 str

        self.question_show = QListWidget(self)
        self.question_show.resize(200, 170)
        self.question_show.move(0, 30)
        if questions:
            for q in questions:
                self.question_show.addItem(self.list2str(q))
        else:
            self.question_show.addItem('当前条件下没有问题生成')
        # self.question_show.itemClicked.connect(self.question_choose)
        
        self.show()
        
    def question_choose(self, item):
        QMessageBox.information(self, "提示", "你选择了: " + item.text().encode('utf-8'), QMessageBox.Ok, QMessageBox.Ok)

    def list2str(self, l):
        return ' '.join(l)
class GUI(QWidget):
     
    def __init__(self):
        super(GUI, self).__init__()
         
        self.initUI()
        self.play = Stick_game(equation=[])
        self.question_database = None
    class Digit():
        # Poverty
        # 1. show number
        # 2. possible to change certain line's color / type

        def __init__(self, loc = (0,0)):
            self.length = 10
            self.width = 4
            self.line_gap = 1
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

        def initUI(self, loc):
            """
            # number encoding order with:
            —— 1
            | 2 | 3
            —— 4
            | 5 | 6
            —— 7
            """
            def line_create():
                line = QPainter()
                line.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                line.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                return line

            self.line1 = QPainter(self)
            self.line1.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            self.line1.setBrush(QBrush(Qt.white, Qt.SolidPattern))
            self.line1.drawRect(loc[0] + self.line_gap + self.width, loc[1], self.length, self.width)

            self.line2 = QPainter(self)
            self.line2.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            self.line2.setBrush(QBrush(Qt.white, Qt.SolidPattern))
            self.line2.drawRect(loc[0], loc[1] + self.line_gap, self.width, self.length)

            self.line3 = QPainter(self)
            self.line3.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            self.line3.setBrush(QBrush(Qt.white, Qt.SolidPattern))
            self.line3.drawRect(loc[0] + 2*self.line_gap + self.length + self.width, loc[1] + self.line_gap, self.width, self.length)

            self.line4 = QPainter(self)
            self.line4.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            self.line4.setBrush(QBrush(Qt.white, Qt.SolidPattern))
            self.line4.drawRect(loc[0] + self.line_gap + self.width, loc[1] + 2*self.line_gap + self.length + self.width, self.length, self.width)

            self.line5 = QPainter(self)
            self.line5.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            self.line5.setBrush(QBrush(Qt.white, Qt.SolidPattern))
            self.line5.drawRect(loc[0], loc[1] + 3*self.line_gap + self.length + 2*self.width, self.width, self.length)

            self.line6 = QPainter(self)
            self.line6.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            self.line6.setBrush(QBrush(Qt.white, Qt.SolidPattern))
            self.line6.drawRect(loc[0] + 2*self.line_gap + self.length + self.width, 
                                loc[1] + 3*self.line_gap + self.length + 2*self.width, self.width, self.length)
            
            self.line7 = QPainter(self)
            self.line7.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            self.line7.setBrush(QBrush(Qt.white, Qt.SolidPattern))
            self.line7.drawRect(loc[0] + self.line_gap + self.width, 
                                loc[1] + 4*self.line_gap + 2*self.length + 2*self.width, self.length, self.width)
            self.lines = [self.line1, self.line2, self.line3, self.line4, self.line5, self.line6, self.line7]

    def initUI(self):
        
        QToolTip.setFont(QFont('SansSerif', 10))

        # question input
        title = QLabel(self)
        title.setText('题目输入：')
        title.move(50, 50)
        hint_in = QLabel(self)
        hint_in.setText('原题：')
        hint_in.move(20, 125)
        hint_out = QLabel(self)
        hint_out.setText('题解：')
        hint_out.move(20, 225)
        self.number1 = QLineEdit(self)
        self.number1.resize(75, 30)
        self.number1.move(150, 50)
        self.number1.textChanged[str].connect(lambda: self.number_update_display(self.number1.text(), 1))
        self.digit1_1 = QLabel(self)
        self.digit1_1.resize(64, 64)
        self.digit1_1.move(100, 100)
        self.digit1_2 = QLabel(self)
        self.digit1_2.resize(64, 64)
        self.digit1_2.move(150, 100)
        self.digit1_1_ans = QLabel(self)
        self.digit1_1_ans.resize(64, 64)
        self.digit1_1_ans.move(100, 200)
        self.digit1_2_ans = QLabel(self)
        self.digit1_2_ans.resize(64, 64)
        self.digit1_2_ans.move(150, 200)

        self.op1 = QComboBox(self)
        self.op1.move(250, 50)
        self.op1.addItems([' ', '+', '-', 'x', '='])
        self.op1.currentIndexChanged[str].connect(lambda: self.op_update_display(self.op1.currentText(), 1))
        # self.op1.highlighted[str].connect(lambda: self.op_update_display(self.op1.activated[str], 1))
        self.op1_show = QLabel(self)
        self.op1_show.resize(32, 32)
        self.op1_show.move(225, 120)
        self.op_show(self.op1.currentText(), self.op1_show)
        self.op1_show_ans = QLabel(self)
        self.op1_show_ans.resize(32, 32)
        self.op1_show_ans.move(225, 220)

        self.number2 = QLineEdit(self)
        self.number2.resize(75, 30)
        self.number2.move(320, 50)
        self.number2.textChanged[str].connect(lambda: self.number_update_display(self.number2.text(), 2))
        self.digit2_1 = QLabel(self)
        self.digit2_1.resize(64, 64)
        self.digit2_1.move(265, 100)
        self.digit2_2 = QLabel(self)
        self.digit2_2.resize(64, 64)
        self.digit2_2.move(315, 100)
        self.digit2_1_ans = QLabel(self)
        self.digit2_1_ans.resize(64, 64)
        self.digit2_1_ans.move(265, 200)
        self.digit2_2_ans = QLabel(self)
        self.digit2_2_ans.resize(64, 64)
        self.digit2_2_ans.move(315, 200)

        self.op2 = QComboBox(self)
        self.op2.move(420, 50)
        self.op2.addItems([' ', '+', '-', 'x', '='])
        self.op2.currentIndexChanged[str].connect(lambda: self.op_update_display(self.op2.currentText(), 2))
        # self.op2.highlighted[str].connect(lambda: self.op_update_display(self.op2.activated[str], 2))
        self.op2_show = QLabel(self)
        self.op2_show.resize(32, 32)
        self.op2_show.move(400, 120)
        self.op_show(self.op2.currentText(), self.op2_show)
        self.op2_show_ans = QLabel(self)
        self.op2_show_ans.resize(32, 32)
        self.op2_show_ans.move(400, 220)

        self.number3 = QLineEdit(self)
        self.number3.resize(75, 30)
        self.number3.move(490, 50)
        self.number3.textChanged[str].connect(lambda: self.number_update_display(self.number3.text(), 3))
        self.digit3_1 = QLabel(self)
        self.digit3_1.resize(64, 64)
        self.digit3_1.move(450, 100)
        self.digit3_2 = QLabel(self)
        self.digit3_2.resize(64, 64)
        self.digit3_2.move(500, 100)
        self.digit3_1_ans = QLabel(self)
        self.digit3_1_ans.resize(64, 64)
        self.digit3_1_ans.move(450, 200)
        self.digit3_2_ans = QLabel(self)
        self.digit3_2_ans.resize(64, 64)
        self.digit3_2_ans.move(500, 200)

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
        btn5.move(600, 50)

        # Button 6: Quit
        qbtn = QPushButton('退出', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(700, 300)
        
        # Background
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('./image/bg.jpg')))
        self.setPalette(palette1)
        self.setAutoFillBackground(True)

        self.center()
        self.resize(800, 400)
        # self.setGeometry(300, 300, 900, 400) # 900*400
        self.setWindowTitle('Stick Game')
        self.setWindowIcon(QIcon('./image/ICON.png'))       
     
        self.show()

    def digit_show(self, number, label):
        # https://www.iconfont.cn/collections/detail?spm=a313x.7781069.0.da5a778a4&cid=1108
        if number == None:
            label.clear()
        else:
            png = QPixmap('./image/%d.png' % number)
            png = png.scaled(64, 64)
            label.setPixmap(png)
    
    def op_show(self, op, label):
        # https://www.iconfont.cn/collections/detail?spm=a313x.7781069.0.da5a778a4&cid=18915
        if op != ' ':
            if op == '+':
                img_path = r'./image/add.png'
            elif op == '-':
                img_path = r'./image/sub.png'
            elif op == 'x':
                img_path = r'./image/mul.png'
            else:
                img_path = r'./image/equal.png'
            png = QPixmap(img_path)
            png = png.scaled(32, 32)
            label.setPixmap(png)
        else:
            label.clear()

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

    def op_update_display(self, op, op_index, is_ans = False):
        if not is_ans:
            if op_index == 1:
                op_show_label = self.op1_show
            else:
                op_show_label = self.op2_show
        else:
            if op_index == 1:
                op_show_label = self.op1_show_ans
            else:
                op_show_label = self.op2_show_ans            
        self.op_show(op, op_show_label)

    def number_update_display(self, number, number_index, is_ans = False):
        if not is_ans:
            if number_index == 1:
                show_digit1 = self.digit1_1
                show_digit2 = self.digit1_2
            elif number_index == 2:
                show_digit1 = self.digit2_1
                show_digit2 = self.digit2_2
            else:
                show_digit1 = self.digit3_1
                show_digit2 = self.digit3_2
        else:
            if number_index == 1:
                show_digit1 = self.digit1_1_ans
                show_digit2 = self.digit1_2_ans
            elif number_index == 2:
                show_digit1 = self.digit2_1_ans
                show_digit2 = self.digit2_2_ans
            else:
                show_digit1 = self.digit3_1_ans
                show_digit2 = self.digit3_2_ans           
        if number is not None:
            try:
                number = int(number)                                
                if number > 99:
                    reply = QMessageBox.information(self, '提示', "请输入两位数字", QMessageBox.Ok, QMessageBox.Ok)
                elif number > 9:
                    # number 2 digits
                    digit1 = number // 10
                    digit2 = number - digit1 * 10
                    self.digit_show(digit1, show_digit1)
                    self.digit_show(digit2, show_digit2)
                else:
                    self.digit_show(None, show_digit1)
                    self.digit_show(number, show_digit2)
            except:
                # clear!
                self.digit_show(None, show_digit1)
                self.digit_show(None, show_digit2)
                print('None')
        else:
            # clear!
            self.digit_show(None, show_digit1)
            self.digit_show(None, show_digit2)
            print('None')
    
    def Solution_Step_One(self):
        self.play.equation_update(['%d' % int(self.number1.text()), self.op1.currentText(), '%d' % int(self.number2.text()), self.op2.currentText(), '%d' % int(self.number3.text())])
        ans = self.play.One_Stick()
        self.solution_info(ans)
    
    def Solution_Step_Two(self):
        self.play.equation_update(['%d' % int(self.number1.text()), self.op1.currentText(), '%d' % int(self.number2.text()), self.op2.currentText(), '%d' % int(self.number3.text())])
        ans = self.play.Two_Stick()
        self.solution_info(ans)

    def solution_info(self, ans):
        if not ans:
            QMessageBox.information(self, '抱歉', "当前条件下，此问题没有解法", QMessageBox.Ok, QMessageBox.Ok)
            self.number_update_display(None, 1, is_ans = True)
            self.number_update_display(None, 2, is_ans = True)
            self.number_update_display(None, 3, is_ans = True)
            self.op_update_display(' ', 1, is_ans = True)
            self.op_update_display(' ', 2, is_ans = True)
        else:
            if len(ans) > 1:
                QMessageBox.information(self, '提示', "已找到%d个解\n将随机选择答案显示" % len(ans), QMessageBox.Ok, QMessageBox.Ok)
                answer = ans[randrange(len(ans))]
            else:
                QMessageBox.information(self, '提示', "已找到1个解", QMessageBox.Ok, QMessageBox.Ok)
                answer = ans[0]
            print(answer)
            self.number_update_display(int(answer[0]), 1, is_ans = True)
            self.number_update_display(int(answer[2]), 2, is_ans = True)
            self.number_update_display(int(answer[4]), 3, is_ans = True)
            self.op_update_display(answer[1], 1, is_ans = True)
            self.op_update_display(answer[3], 2, is_ans = True)
    
    def Generation_Ground_truth(self):
        reply = QMessageBox.question(self, '提示',
            "若以当前输入等式为答案生成问题，请选Yes\n否则，随机生成答案与问题", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
 
        if reply == QMessageBox.Yes:
            if self.number1.text() and self.number2.text() and self.number3.text():
                tmp_equation = ['%d' % int(self.number1.text()), self.op1.currentText(), '%d' % int(self.number2.text()), self.op2.currentText(), '%d' % int(self.number3.text())]
                if self.play.equation_satisfy(tmp_equation):
                    return tmp_equation
                else:
                    QMessageBox.warning(self, '注意', "当前输入等式不满足，无法将其作为答案\n现在随机生成", QMessageBox.Ok, QMessageBox.Ok)
                    return None
            else:
                QMessageBox.warning(self, '注意', "当前输入等式不满足，无法将其作为答案\n现在随机生成", QMessageBox.Ok, QMessageBox.Ok)
                return None
        else:
            return None
    
    def Generation_Step_One(self):
        given_equation = self.Generation_Ground_truth()
        questions, equation_true = self.play.question_generate(is_generate_two=False, given_equation=given_equation)
        self.question_show = Question_GUI(parent=None, ans=equation_true, questions=questions)

    def Generation_Step_Two(self):
        given_equation = self.Generation_Ground_truth()
        questions, equation_true = self.play.question_generate(is_generate_two=True, given_equation=given_equation)
        self.question_show = Question_GUI(parent=None, ans=equation_true, questions=questions)

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