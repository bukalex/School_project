# -*- coding: utf-8 -*-
import time
from math import sqrt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog
from utils import Chastica, Reshetka, Ellipse, Line
from graphics import Energy
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsSimpleTextItem
#from matplotlib.figure import Figure
import sys


class Processy():           #
    def __init__(self, resh, radio_check, a, b, window):
        while True:         # запуск цикла
            if resh.matrix[0][0].ell.pause == False:                # отслеживается состояние кнопки "остановить"
                time.sleep(0.05)                                    # частота кадров
                resh.step()                                         # пересчет данных
                window.move_graphics(resh.matrix)                   # обновление изображения
                QtWidgets.qApp.processEvents()
            else:
                break

    
class View():
    def __init__(self):
        self.window = QtWidgets.QWidget()           # создание главного окна
        self.window.resize(1250, 1000)
        self.window.setWindowTitle('Кристалл Гука')
        
        self.scene = QtWidgets.QGraphicsScene(250, 0, 1000, 1000, self.window)           # создание графической сцены
        self.view = QtWidgets.QGraphicsView(self.window)
        self.view.setGeometry(250, 0, 1000, 1000)           # задаем видимую часть сцены
        self.view.setScene(self.scene)

        self.btn_start = QtWidgets.QPushButton('&Запустить', self.window)           # кнопка запуска
        self.btn_start.clicked.connect(self.start)
        self.btn_stop = QtWidgets.QPushButton('&Остановить', self.window)           # кнопка паузы
        self.btn_stop.clicked.connect(self.stop)
        self.btn_graph = QtWidgets.QPushButton('&Графики', self.window)           # кнопка для вывода графиков
        self.btn_graph.clicked.connect(self.create_dialogwindow)
        self.btn_help = QtWidgets.QPushButton('&Справка', self.window)           # справка
        self.btn_help.clicked.connect(self.help_dialogwindow)

        self.font = QtGui.QFont("Times", 11, QtGui.QFont.Bold)
        self.btn_start.setFont(self.font)
        self.btn_stop.setFont(self.font)
        self.btn_graph.setFont(self.font)
        self.btn_help.setFont(self.font)
        
        self.btn_start.setGeometry(50, 25, 150, 40)
        self.btn_stop.setGeometry(50, 70, 150, 40)
        self.btn_graph.setGeometry(50, 115, 150, 40)
        self.btn_help.setGeometry(50, 950, 150, 40)
        
        self.btn_start_pressed = False           # флаг для проверки состояния кнопки "старт"
        self.btn_stop.setEnabled(False)           # делаем кнопку паузы неактивной
        self.btn_start.setEnabled(False)           # делаем кнопку запуска неактивной
        self.btn_graph.setEnabled(False)           # делаем кнопку запуска графиков неактивной
        
        self.vvod_a_b_m_k_l_dt = [QtWidgets.QSpinBox(self.window) for i in range(2)]           # создание полей ввода исходных данных
        for i in range(4):
            self.vvod = QtWidgets.QDoubleSpinBox(self.window)
            self.vvod_a_b_m_k_l_dt.append(self.vvod)
        for i in range(len(self.vvod_a_b_m_k_l_dt)):
            self.vvod_a_b_m_k_l_dt[i].setGeometry(5, 125+50*(i+1), 240, 30)
            self.vvod_a_b_m_k_l_dt[i].setRange(0, 1000)
        self.vvod_a_b_m_k_l_dt[0].setMinimum(3)
        self.vvod_a_b_m_k_l_dt[1].setMinimum(3)
        self.vvod.setDecimals(4)
        self.vvod.setMinimum(0.0001)
        self.vvod.setMaximum(0.0012)
        
        self.vvod_a_b_m_k_l_dt[0].setValue(5)           # задаем исходные данные
        self.vvod_a_b_m_k_l_dt[1].setValue(5)
        self.vvod_a_b_m_k_l_dt[2].setValue(93)
        self.vvod_a_b_m_k_l_dt[3].setValue(5)
        self.vvod_a_b_m_k_l_dt[4].setValue(100)
        self.vvod_a_b_m_k_l_dt[5].setValue(0.0008)
        
        self.vvod_a_b_m_k_l_dt[0].setPrefix('Высота сетки: ')
        self.vvod_a_b_m_k_l_dt[1].setPrefix('Ширина сетки: ')
        self.vvod_a_b_m_k_l_dt[2].setPrefix('Масса частиц, *10^-27 кг: ')
        self.vvod_a_b_m_k_l_dt[3].setPrefix('Жесткость пружин, *10^-20 н/м: ')
        self.vvod_a_b_m_k_l_dt[4].setPrefix('Начальное расстояние, *10^-11 м: ')
        self.vvod_a_b_m_k_l_dt[5].setPrefix('Промежуток времени, с: ')
        
        self.vvod_a_b_m_k_l_dt[0].setSingleStep(1)
        self.vvod_a_b_m_k_l_dt[1].setSingleStep(1)
        self.vvod_a_b_m_k_l_dt[2].setSingleStep(1)
        self.vvod_a_b_m_k_l_dt[3].setSingleStep(0.1)
        self.vvod_a_b_m_k_l_dt[4].setSingleStep(10)
        self.vvod_a_b_m_k_l_dt[5].setSingleStep(0.0001)

        self.a = self.vvod_a_b_m_k_l_dt[0].value()
        self.b = self.vvod_a_b_m_k_l_dt[1].value()
        self.m = self.vvod_a_b_m_k_l_dt[2].value()*10**(-27)
        self.k = self.vvod_a_b_m_k_l_dt[3].value()*10**(-20)
        self.l = self.vvod_a_b_m_k_l_dt[4].value()
        self.dt = self.vvod_a_b_m_k_l_dt[5].value()

        self.radio_3_4_6 = [QtWidgets.QRadioButton(self.window) for i in range(3)]           # создание радиокнопок для смены формы ячеек
        self.radio_3_4_6[1].setChecked(True)
        self.radio_check = [False, True, False]
        self.radio_group = QtWidgets.QGroupBox('Выберите форму элементарной ячейки:', self.window)
        self.radio_group.setGeometry(10, 500, 230, 350)
        self.vbox = QtWidgets.QVBoxLayout(self.window)
        self.images = [QtGui.QPixmap('images\треугольник'), QtGui.QPixmap('images\квадрат.png'), QtGui.QPixmap('images\шестиугольник.png')]
        for i in range(len(self.radio_3_4_6)):
            self.radio_3_4_6[i].toggled.connect(self.radiobutton)
            self.icon = QtGui.QIcon(self.images[i])
            self.radio_3_4_6[i].setIcon(self.icon)
            self.radio_3_4_6[i].setIconSize(QtCore.QSize(100, 100))
            self.vbox.addWidget(self.radio_3_4_6[i])
        self.radio_group.setLayout(self.vbox)
        for i in self.vvod_a_b_m_k_l_dt:
            i.valueChanged.connect(self.options)
        self.draw()           # выводим изображение на сцену
        self.window.show()

        self.help_dialogwindow()

    def radiobutton(self):           # метод, меняющий форму ячеек
        self.resh.matrix[0][0].ell.pause = True
        self.scene.clear()
        for i in range(len(self.radio_3_4_6)):
            self.radio_check[i]=self.radio_3_4_6[i].isChecked()
        self.draw()
        self.btn_stop.setEnabled(False)
        self.btn_start_pressed = False
        self.btn_start.setEnabled(False)
        self.btn_start.setText('&Запустить')
        self.btn_stop.setText('&Остановить')
        for i in self.vvod_a_b_m_k_l_dt:
                i.setEnabled(True)


    def options(self):           # изменение значений переменных при работе с полями ввода
        if not self.btn_start_pressed:
            self.a = self.vvod_a_b_m_k_l_dt[0].value()           # число строк в сетке
            self.b = self.vvod_a_b_m_k_l_dt[1].value()           # чисто столбцов в сетке
            self.m = self.vvod_a_b_m_k_l_dt[2].value()*10**(-27)           # масса частиц
            self.k = self.vvod_a_b_m_k_l_dt[3].value()*10**(-20)           # коэффициент жесткости пружин
            self.l = self.vvod_a_b_m_k_l_dt[4].value()           # длина нерастянутой пружины
            self.dt = self.vvod_a_b_m_k_l_dt[5].value()             # промежуток времени
            self.btn_start.setEnabled(False)
            self.scene.clear()
            self.draw()

    def start(self):           # запуск процессов/сброс
        if not self.btn_start_pressed:
            self.btn_start_pressed = True
            self.btn_stop.setEnabled(True)
            self.btn_graph.setEnabled(True)
            self.btn_stop.setText('&Остановить')
            self.btn_start.setText('&Сброс')
            for i in self.vvod_a_b_m_k_l_dt:
                i.setEnabled(False)
            for i in range(self.a):
                for j in range(self.b):
                    self.resh.matrix[i][j].ell.pause = False
                    self.resh.matrix[i][j].setEnabled(False)
            for i in self.resh.lines:
                self.scene.removeItem(i)
            self.programm = Processy(self.resh, self.radio_check, self.a, self.b, self)           # переход в основной цикл

        else:
            self.radiobutton()

    def move_graphics(self, matrix):            # перемещение изображений
        if self.resh.matrix[0][0].ell.pause == False:
            for i in self.lines_list:
                self.scene.removeItem(i)
            self.lines_list=[]
            for i in self.resh.lines:
                self.line = QtWidgets.QGraphicsLineItem(i.line.x1, i.line.y1, i.line.x2, i.line.y2)
                self.lines_list.append(self.line)
                self.scene.addItem(self.line)
            for i in range(self.a):
                for j in range(self.b):
                    x = matrix[i][j].ell.x-matrix[i][j].ell.x_
                    y = matrix[i][j].ell.y-matrix[i][j].ell.y_
                    self.resh.matrix[i][j].moveBy(x, y)
            self.M_center = QGraphicsEllipseItem(sum(self.resh.list_Mx)/len(self.resh.list_Mx)+300, sum(self.resh.list_My)/len(self.resh.list_My)+50, 10, 10)           # метки, указывающие на положение центра энергии
            self.M_center.setBrush(QtGui.QBrush(QtGui.QColor(200,0,0), style = QtCore.Qt.SolidPattern))
            self.scene.addItem(self.M_center)
            self.center_list.append(self.M_center)
            self.M_center_now = QGraphicsEllipseItem(self.resh.list_Mx[-1]+300, self.resh.list_My[-1]+50, 10, 10)
            self.M_center_now.setBrush(QtGui.QBrush(QtGui.QColor(0,200,0), style = QtCore.Qt.SolidPattern))
            self.scene.addItem(self.M_center_now)
            self.now_center_list.append(self.M_center_now)
            if len(self.center_list) > 1:
                self.scene.removeItem(self.center_list[0])
                self.center_list.pop(0)
                self.scene.removeItem(self.now_center_list[0])
                self.now_center_list.pop(0)

    def stop(self):           # остановка/продолжение всех процессов
        for i in range(self.a):
            for j in range(self.b):
                self.resh.matrix[i][j].ell.pause = not self.resh.matrix[i][j].ell.pause
        if self.resh.matrix[0][0].ell.pause == True:
            self.btn_stop.setText('&Продолжить')
        else:
            self.btn_stop.setText('&Остановить')
            self.programm = Processy(self.resh, self.radio_check, self.a, self.b, self)

    def draw(self):           # вывод изображения на сцену
        self.resh = Reshetka(self.a, self.b, self.dt, self.l, self.k, self.m, self.radio_check, self)           # создание новой решетки
        self.lines_list=[]
        self.center_list = []
        self.now_center_list = []
        for i in range(self.a):
            for j in range(self.b):
                self.resh.matrix[i][j].setBrush(QtGui.QBrush(self.resh.matrix[i][j].color, style = QtCore.Qt.SolidPattern))
                self.scene.addItem(self.resh.matrix[i][j])
        for i in self.resh.lines:
            self.lines_list.append(i)
            self.scene.addItem(i)

        for i in range(self.a):             # нанесение разметки (координаты)
            self.text = QGraphicsSimpleTextItem(str(round(self.resh.matrix[i][0].ell.y-50)))
            self.text.setPos(270, self.resh.matrix[i][0].ell.y+20)
            self.scene.addItem(self.text)
        for i in range(self.b):
            self.text = QGraphicsSimpleTextItem(str(round(self.resh.matrix[0][i].ell.x-300)))
            self.text.setPos(self.resh.matrix[0][i].ell.x+15, self.resh.matrix[0][i].ell.y-30)
            self.scene.addItem(self.text)

    def create_dialogwindow(self):           # вывод графиков в диалоговом окне
        self.graph = Energy(self.resh.list_Wp, self.resh.list_Wk, self.resh.list_W, self.resh.list_Mx, self.resh.list_My , self.resh.list_t, self.resh.t)
        result = self.graph.exec()

    def help_dialogwindow(self):
        self.help = QDialog()
        self.help.resize(700, 450)
        self.help.setWindowTitle('Справка')
        self.file = open("help.txt", 'r', encoding='utf-8')
        self.file_lines_list = self.file.readlines()
        for i in self.file_lines_list:
            self.text = QtWidgets.QLabel(i, self.help)
            self.font = QtGui.QFont("Times", 11, QtGui.QFont.Bold)           # изменение шрифта
            self.text.setFont(self.font)
            self.text.setGeometry(20, 20*(1+self.file_lines_list.index(i)), 660, 18)
        self.file.close()
        result = self.help.exec()


class Names(QDialog):           # вывод заставки
    def __init__(self):
        super().__init__()
        self.resize(500, 300)
        self.setWindowTitle('Заставка')
        self.name = QtWidgets.QLabel('Кристалл Гука', self)           # создание текста
        self.author = QtWidgets.QLabel('Автор проекта:\nГурылев Алексей 10-4', self)
        self.manager = QtWidgets.QLabel('Руководитель проекта:\nКондратенко Федор Игоревич', self)
        self.button = QtWidgets.QPushButton('&Продолжить', self)
        self.button.clicked.connect(self.start)

        self.font = QtGui.QFont("Times", 18, QtGui.QFont.Bold)           # изменение шрифта
        self.name.setFont(self.font)
        self.author.setFont(self.font)
        self.manager.setFont(self.font)
        self.button.setFont(self.font)
        
        self.name.setGeometry(50, 0, 400, 60)           # размещение текста
        self.author.setGeometry(50, 70, 400, 60)
        self.manager.setGeometry(50, 140, 400, 60)
        self.button.setGeometry(100, 250, 300, 50)
        self.show()

    def start(self):           # переход к главному окну приложения
        self.hide()
        self.window = View()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)           # создание приложения
    start_window = Names()           # заставка
    sys.exit(app.exec_())           # завершения работы приложения
