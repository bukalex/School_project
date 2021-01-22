# -*- coding: utf-8 -*-
import time
from math import sqrt
from PyQt5 import QtWidgets
import sys


class processy():
    def __init__(self, resh, window):
        while True:         #запуск цикла
        #for i in range(10):
            time.sleep(0.005)
            resh.step()
            window.move_graphics(resh.matrix)  # обновление изображения
            QtWidgets.qApp.processEvents()

    
class view():
    def __init__(self):
        self.window = QtWidgets.QWidget()
        self.window.resize(1250, 1000)
        
        self.scene = QtWidgets.QGraphicsScene(250, 0, 1000, 1000, self.window)
        self.view = QtWidgets.QGraphicsView(self.window)
        self.view.setGeometry(250, 0, 1000, 1000)
        self.view.setScene(self.scene)
        
        self.opt_scene = QtWidgets.QGraphicsScene(0, 0, 250, 1000, self.window)
        self.opt_view = QtWidgets.QGraphicsView(self.window)
        self.opt_view.setGeometry(0, 0, 250, 1000)
        self.opt_view.setScene(self.opt_scene)
        
        self.btn_start = QtWidgets.QPushButton('&Запуск')
        self.btn_start.clicked.connect(self.options)
        self.vvod_a_b_m_k_l_dt = []
        for i in range(5):
            self.vvod = QtWidgets.QSpinBox()
            self.vvod_a_b_m_k_l_dt.append(self.vvod)
        self.vvod = QtWidgets.QDoubleSpinBox()
        self.vvod_a_b_m_k_l_dt.append(self.vvod)
        self.btn_start.setGeometry(50, 50, 150, 50)
        for i in range(len(self.vvod_a_b_m_k_l_dt)):
            self.vvod_a_b_m_k_l_dt[i].setGeometry(25, 50+75*(i+1), 200, 30)
            self.vvod_a_b_m_k_l_dt[i].setRange(0, 1000000)
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
        
        self.opt_scene.addWidget(self.btn_start)
        for i in self.vvod_a_b_m_k_l_dt:
            self.opt_scene.addWidget(i)

        self.radio_3 = QtWidgets.QRadioButton()
        self.radio_4 = QtWidgets.QRadioButton()
        self.radio_6 = QtWidgets.QRadioButton()
        self.radio_group = QtWidgets.QGroupBox('Выберите форму элементарной ячейки:')
        self.radio_group.setGeometry(10, 600, 230, 200)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.radio_3)
        self.vbox.addWidget(self.radio_4)
        self.vbox.addWidget(self.radio_6)
        self.radio_group.setLayout(self.vbox)
        self.opt_scene.addWidget(self.radio_group)
        
        self.window.show()

    def options(self):
        self.a = self.vvod_a_b_m_k_l_dt[0].value()
        self.b = self.vvod_a_b_m_k_l_dt[1].value()
        self.m = self.vvod_a_b_m_k_l_dt[2].value()           #масса частиц
        self.k = self.vvod_a_b_m_k_l_dt[3].value()           #коэффициент жесткости пружин
        self.l = self.vvod_a_b_m_k_l_dt[4].value()           #длина нерастянутой пружины
        self.dt = self.vvod_a_b_m_k_l_dt[5].value()         #промежуток времени
        self.start()

    def start(self):
        self.scene.clear()
        resh = reshetka(self.a, self.b, self.dt, self.l, self.k, self.m)
        resh.displacement(1, 1, [2, -2])
        self.ellipse = []
        for i in range(self.a):          #загрузка изображений на сцену
            for j in range(self.b):
                self.ell = QtWidgets.QGraphicsEllipseItem(300, 100, 50, 50)
                self.scene.addItem(self.ell)
                self.ell.setPos(resh.matrix[i][j].x, resh.matrix[i][j].y)
                self.ellipse.append(self.ell)
        self.programm = processy(resh, self)

    def move_graphics(self, matrix):            #перемещение изображений
        for i in range(self.a):
            for j in range(self.b):
                x = matrix[i][j].x-matrix[i][j]._x_
                y = matrix[i][j].y-matrix[i][j]._y_
                self.ellipse[i*self.b+j].moveBy(x, y)
                

class chastica():
    def __init__(self, m, i, j, k, l):
        self.m = m
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.Vx = 0
        self.Vy = 0
        self.x = l*j
        self.y = l*i
        self.z = 0
        self._x_ = self.x
        self._y_ = self.y
        self._z_ = self.z
        self.Fx = 0
        self.Fy = 0

    def sily(self, particles):
        self.Fx = 0
        self.Fy = 0
        for part in particles:
            d = sqrt((part.x-self.x)**2+(part.y-self.y)**2)
            if d != 0:
                dx = (d-self.l)*(part.x-self.x)/d
                dy = (d-self.l)*(part.y-self.y)/d
                self.Fx += self.k*(d-self.l)*(part.x-self.x)/d
                self.Fy += self.k*(d-self.l)*(part.y-self.y)/d

    def move(self,dt):
        _x_ = self._x_
        _y_ = self._y_
        self._x_ = self.x
        self._y_ = self.y
        self.x = 2*self.x-_x_+(self.Fx/self.m)*(dt**2)
        self.y = 2*self.y-_y_+(self.Fy/self.m)*(dt**2)
        
        
class reshetka():
    def __init__(self, a, b, dt, l, k, m):
        self.a = a
        self.b = b
        self.dt = dt
        self.l = l
        self.k = k
        self.m = m
        self.matrix = self.create_matrix()

    def create_matrix(self):
        return [[chastica(self.m, i, j, self.k, self.l) for j in range(self.b)] for i in range(self.a)]

    def displacement(self, i, j, displ):
        self.matrix[i][j].x += displ[0]
        self.matrix[i][j].y += displ[1]

    def step(self):
        for i in range(1, self.a-1):
            for j in range(1, self.b-1):
                particles = self.get_neighbours(i, j)
                self.matrix[i][j].sily(particles)
        for i in range(1, self.a-1):
            for j in range(1, self.b-1):
                self.matrix[i][j].move(self.dt)

    def get_neighbours(self, i, j):
        particles = []
        for n in range(3):
            for nn in range(3):
                particles.append(self.matrix[i+n-1][j+nn-1])
        return particles


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = view()
    sys.exit(app.exec_())
