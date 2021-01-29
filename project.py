# -*- coding: utf-8 -*-
import time
from math import sqrt
from PyQt5 import QtWidgets, QtGui, QtCore
from utils import Chastica, Reshetka
import sys


class Processy():
    def __init__(self, resh, window):
        while True:         #запуск цикла
        #for i in range(10):
            time.sleep(0.005)
            resh.step()
            window.move_graphics(resh.matrix)  # обновление изображения
            QtWidgets.qApp.processEvents()

    
class View():
    def __init__(self):
        self.window = QtWidgets.QWidget()
        self.window.resize(1250, 1000)
        
        self.scene = QtWidgets.QGraphicsScene(250, 0, 1000, 1000, self.window)
        self.view = QtWidgets.QGraphicsView(self.window)
        self.view.setGeometry(250, 0, 1000, 1000)
        self.view.setScene(self.scene)

        self.btn_start = QtWidgets.QPushButton('&Запустить', self.window)
        self.btn_start.clicked.connect(self.options)
        self.btn_stop = QtWidgets.QPushButton('&Остановить', self.window)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_start.setGeometry(50, 25, 150, 40)
        self.btn_stop.setGeometry(50, 70, 150, 40)
        self.btn_start_pressed = False
        self.btn_stop.setEnabled(False)
        
        self.vvod_a_b_m_k_l_dt = [QtWidgets.QSpinBox(self.window) for i in range(5)]
        self.vvod = QtWidgets.QDoubleSpinBox(self.window)
        self.vvod_a_b_m_k_l_dt.append(self.vvod)
        for i in range(len(self.vvod_a_b_m_k_l_dt)):
            self.vvod_a_b_m_k_l_dt[i].setGeometry(25, 50+75*(i+1), 200, 30)
            self.vvod_a_b_m_k_l_dt[i].setRange(-1, 1000000)
        self.vvod_a_b_m_k_l_dt[0].setMinimum(3)
        self.vvod_a_b_m_k_l_dt[1].setMinimum(3)
        self.vvod.setDecimals(3)
        
        self.vvod_a_b_m_k_l_dt[0].setValue(5)
        self.vvod_a_b_m_k_l_dt[1].setValue(5)
        self.vvod_a_b_m_k_l_dt[2].setValue(100)
        self.vvod_a_b_m_k_l_dt[3].setValue(50000)
        self.vvod_a_b_m_k_l_dt[4].setValue(100)
        self.vvod_a_b_m_k_l_dt[5].setValue(0.001)
        
        self.vvod_a_b_m_k_l_dt[0].setPrefix('Высота сетки: ')
        self.vvod_a_b_m_k_l_dt[1].setPrefix('Ширина сетки: ')
        self.vvod_a_b_m_k_l_dt[2].setPrefix('Масса частиц: ')
        self.vvod_a_b_m_k_l_dt[3].setPrefix('Жесткость пружин: ')
        self.vvod_a_b_m_k_l_dt[4].setPrefix('Начальное расстояние: ')
        self.vvod_a_b_m_k_l_dt[5].setPrefix('Промежуток времени: ')
        
        self.vvod_a_b_m_k_l_dt[0].setSingleStep(1)
        self.vvod_a_b_m_k_l_dt[1].setSingleStep(1)
        self.vvod_a_b_m_k_l_dt[2].setSingleStep(5)
        self.vvod_a_b_m_k_l_dt[3].setSingleStep(500)
        self.vvod_a_b_m_k_l_dt[4].setSingleStep(10)
        self.vvod_a_b_m_k_l_dt[5].setSingleStep(0.001)

        self.a = self.vvod_a_b_m_k_l_dt[0].value()
        self.b = self.vvod_a_b_m_k_l_dt[1].value()
        self.m = self.vvod_a_b_m_k_l_dt[2].value()
        self.k = self.vvod_a_b_m_k_l_dt[3].value()
        self.l = self.vvod_a_b_m_k_l_dt[4].value()
        self.dt = self.vvod_a_b_m_k_l_dt[5].value()

        self.radio_3_4_6 = [QtWidgets.QRadioButton(self.window) for i in range(3)]
        self.radio_3_4_6[1].setChecked(True)
        self.radio_check = [False, True, False]
        self.radio_group = QtWidgets.QGroupBox('Выберите форму элементарной ячейки:', self.window)
        self.radio_group.setGeometry(10, 600, 230, 350)
        self.vbox = QtWidgets.QVBoxLayout(self.window)
        self.images = [QtGui.QPixmap('images\треугольник'), QtGui.QPixmap('images\квадрат.png'), QtGui.QPixmap('images\шестиугольник.png')]
        for i in range(len(self.radio_3_4_6)):
            self.radio_3_4_6[i].toggled.connect(self.radiobutton)
            self.icon = QtGui.QIcon(self.images[i])
            self.radio_3_4_6[i].setIcon(self.icon)
            self.radio_3_4_6[i].setIconSize(QtCore.QSize(100, 100))
            self.vbox.addWidget(self.radio_3_4_6[i])
        self.radio_group.setLayout(self.vbox)

        self.resh = Reshetka(self.a, self.b, self.dt, self.l, self.k, self.m, self.radio_check)
        self.ellipse = []
        for i in range(self.a):
            for j in range(self.b):
                self.ell = QtWidgets.QGraphicsEllipseItem(300, 100, 50, 50)
                self.ell.setPos(self.resh.matrix[i][j].x, self.resh.matrix[i][j].y)
                self.ellipse.append(self.ell)
                self.scene.addItem(self.ell)
        
        self.window.show()

    def radiobutton(self):
        if not self.btn_start_pressed:
            self.scene.clear()
            for i in range(len(self.radio_3_4_6)):
                self.radio_check[i]=self.radio_3_4_6[i].isChecked()
            self.resh = Reshetka(self.a, self.b, self.dt, self.l, self.k, self.m, self.radio_check)
            self.ellipse = []
            for i in range(self.a):
                for j in range(self.b):
                    self.ell = QtWidgets.QGraphicsEllipseItem(300, 100, 50, 50)
                    self.ell.setPos(self.resh.matrix[i][j].x, self.resh.matrix[i][j].y)
                    self.ellipse.append(self.ell)
                    self.scene.addItem(self.ell)

    def options(self):
        self.a = self.vvod_a_b_m_k_l_dt[0].value()
        self.b = self.vvod_a_b_m_k_l_dt[1].value()
        self.m = self.vvod_a_b_m_k_l_dt[2].value()           #масса частиц
        self.k = self.vvod_a_b_m_k_l_dt[3].value()           #коэффициент жесткости пружин
        self.l = self.vvod_a_b_m_k_l_dt[4].value()           #длина нерастянутой пружины
        self.dt = self.vvod_a_b_m_k_l_dt[5].value()         #промежуток времени
        for i in range(len(self.radio_3_4_6)):
            self.radio_check[i]=self.radio_3_4_6[i].isChecked()
        self.start()

    def start(self):
        self.btn_start_pressed = True
        self.scene.clear()
        self.btn_stop.setEnabled(True)
        self.btn_stop.setText('&Остановить')
        self.resh = Reshetka(self.a, self.b, self.dt, self.l, self.k, self.m, self.radio_check)
        self.resh.displacement(1, 1, [1, -1])
        self.ellipse = []
        for i in range(self.a):          #загрузка изображений на сцену
            for j in range(self.b):
                self.resh.matrix[i][j].pause = False
                self.ell = QtWidgets.QGraphicsEllipseItem(300, 100, 50, 50)
                self.ell.setPos(self.resh.matrix[i][j].x, self.resh.matrix[i][j].y)
                self.ellipse.append(self.ell)
                self.scene.addItem(self.ell)
        self.programm = Processy(self.resh, self)

    def move_graphics(self, matrix):            #перемещение изображений
        if self.resh.matrix[0][0].pause == False:
            for i in range(self.a):
                for j in range(self.b):
                    x = matrix[i][j].x-matrix[i][j]._x_
                    y = matrix[i][j].y-matrix[i][j]._y_
                    self.ellipse[i*self.b+j].moveBy(x, y)

    def stop(self):
        self.dt = self.vvod_a_b_m_k_l_dt[5].value()
        self.resh.dt = self.dt
        for i in range(self.a):
            for j in range(self.b):
                self.resh.matrix[i][j].pause = not self.resh.matrix[i][j].pause
        if self.resh.matrix[0][0].pause == True:
            self.btn_stop.setText('&Продолжить')
        else:
            self.btn_stop.setText('&Остановить')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = View()
    sys.exit(app.exec_())
