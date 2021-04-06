# -*- coding: utf-8 -*-
import time
from math import sqrt
from PyQt5 import QtWidgets, QtGui, QtCore
import matplotlib.pyplot as plt
from utils import Chastica, Reshetka, Ellipse, Line
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtGui import QMouseEvent
import sys


class Processy():
    def __init__(self, resh, graph, radio_check, a, b, window):
        #for i in range(300):
        while True:         # запуск цикла
            if resh.matrix[0][0].ell.pause == False:
                time.sleep(0.005)
                if resh.matrix[0][0].ell.pause == False:
                    graph.update(resh.Wp, resh.Wk, resh.W)    # обновление графика
                resh.step()                                         # пересчет данных
                window.move_graphics(resh.matrix)                   # обновление изображения
                QtWidgets.qApp.processEvents()
            else:
                break

    
class View():
    def __init__(self):
        self.window = QtWidgets.QWidget()
        self.window.resize(1250, 1000)
        
        self.scene = QtWidgets.QGraphicsScene(250, 0, 1000, 1000, self.window)
        self.view = QtWidgets.QGraphicsView(self.window)
        self.view.setGeometry(250, 0, 1000, 1000)
        self.view.setScene(self.scene)

        self.btn_start = QtWidgets.QPushButton('&Запустить', self.window)
        self.btn_start.clicked.connect(self.start)
        self.btn_stop = QtWidgets.QPushButton('&Остановить', self.window)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_start.setGeometry(50, 25, 150, 40)
        self.btn_stop.setGeometry(50, 70, 150, 40)
        self.btn_start_pressed = False
        self.btn_stop.setEnabled(False)
        
        self.vvod_a_b_m_k_l_dt = [QtWidgets.QSpinBox(self.window) for i in range(2)]
        for i in range(4):
            self.vvod = QtWidgets.QDoubleSpinBox(self.window)
            self.vvod_a_b_m_k_l_dt.append(self.vvod)
        for i in range(len(self.vvod_a_b_m_k_l_dt)):
            self.vvod_a_b_m_k_l_dt[i].setGeometry(25, 50+75*(i+1), 200, 30)
            self.vvod_a_b_m_k_l_dt[i].setRange(-1, 10**8)
        self.vvod_a_b_m_k_l_dt[0].setMinimum(3)
        self.vvod_a_b_m_k_l_dt[1].setMinimum(3)
        self.vvod.setDecimals(4)
        
        self.vvod_a_b_m_k_l_dt[0].setValue(5)
        self.vvod_a_b_m_k_l_dt[1].setValue(5)
        self.vvod_a_b_m_k_l_dt[2].setValue(100)
        self.vvod_a_b_m_k_l_dt[3].setValue(5*10**7)
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
        for i in self.vvod_a_b_m_k_l_dt:
            i.valueChanged.connect(self.options)
        self.draw()
        self.window.show()

    def radiobutton(self):
        self.resh.matrix[0][0].ell.pause = True
        self.scene.clear()
        for i in range(len(self.radio_3_4_6)):
            self.radio_check[i]=self.radio_3_4_6[i].isChecked()
        self.draw()
        self.btn_stop.setEnabled(False)
        self.btn_start_pressed = False
        self.btn_start.setEnabled(True)


    def options(self):
        if not self.btn_start_pressed:
            self.a = self.vvod_a_b_m_k_l_dt[0].value()
            self.b = self.vvod_a_b_m_k_l_dt[1].value()
            self.m = self.vvod_a_b_m_k_l_dt[2].value()           #масса частиц
            self.k = self.vvod_a_b_m_k_l_dt[3].value()           #коэффициент жесткости пружин
            self.l = self.vvod_a_b_m_k_l_dt[4].value()           #длина нерастянутой пружины
            self.dt = self.vvod_a_b_m_k_l_dt[5].value()         #промежуток времени
            self.scene.clear()
            self.draw()

    def start(self):
        self.graph = Graph(self.dt)
        self.btn_start_pressed = True
        self.btn_stop.setEnabled(True)
        self.btn_start.setEnabled(False)
        self.btn_stop.setText('&Остановить')
        for i in range(self.a):
            for j in range(self.b):
                self.resh.matrix[i][j].ell.pause = False
                
        self.programm = Processy(self.resh, self.graph, self.radio_check, self.a, self.b, self)

    def move_graphics(self, matrix):            #перемещение изображений
        if self.resh.matrix[0][0].ell.pause == False:
            for i in self.lines_list:
                self.scene.removeItem(i)
            self.lines_list=[]
            for i in self.resh.lines:
                self.line = QtWidgets.QGraphicsLineItem(i.x1, i.y1, i.x2, i.y2)
                self.lines_list.append(self.line)
                self.scene.addItem(self.line)
            for i in range(self.a):
                for j in range(self.b):
                    x = matrix[i][j].ell.x-matrix[i][j].ell.x_
                    y = matrix[i][j].ell.y-matrix[i][j].ell.y_
                    self.ellipse[i*self.b+j].moveBy(x, y)

    def stop(self):
        self.dt = self.vvod_a_b_m_k_l_dt[5].value()
        self.resh.dt = self.dt
        for i in range(self.a):
            for j in range(self.b):
                self.resh.matrix[i][j].ell.pause = not self.resh.matrix[i][j].ell.pause
        if self.resh.matrix[0][0].ell.pause == True:
            self.btn_stop.setText('&Продолжить')
        else:
            self.btn_stop.setText('&Остановить')
            self.programm = Processy(self.resh, self.graph, self.radio_check, self.a, self.b, self)

    def draw(self):
        self.resh = Reshetka(self.a, self.b, self.dt, self.l, self.k, self.m, self.radio_check)
        self.ellipse = []
        self.lines_list=[]
        for i in range(self.a):
            for j in range(self.b):
                self.ellipse.append(self.resh.matrix[i][j])
                self.resh.matrix[i][j].setBrush(QtGui.QBrush(self.resh.matrix[i][j].color, style = QtCore.Qt.SolidPattern))
                self.scene.addItem(self.resh.matrix[i][j])
        for i in self.resh.lines:
            self.line = Line(i.x1, i.y1, i.x2, i.y2)
            self.lines_list.append(self.line)
            self.scene.addItem(self.line)
                    

class Graph(FigureCanvas):
    def __init__(self, dt):
        self.list_Wp = [0 for i in range(10)]
        self.list_Wk = [0 for i in range(10)]
        self.list_W = [0 for i in range(10)]

        self.dt = dt
        self.list_t = [self.dt*i for i in range(10)]
        self.t = 0

        self.fig, self.WT = plt.subplots()
        plt.show()

    '''def __init__(self, dt, parent=None, width=50, height=50, dpi=100):
        print('1')
        fig = Figure(figsize=(width, height), dpi=dpi)
        print('2')

        FigureCanvas.__init__(self, fig)
        print('3')
        #self.setParent(parent)
        print('4')

        #FigureCanvas.setSizePolicy(self,
        #                           QSizePolicy.Expanding,
        #                           QSizePolicy.Expanding)
        print('5')
        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor((159 / 255, 212 / 255, 251 / 255))
        self.ax1 = self.figure.add_axes(self.ax.get_position(), frameon=False)
        print('6')
        #self.ax.grid()
        print('7')
        self.draw()
        print('8')'''

    def update(self, Wp, Wk, W):
        pass
        self.list_Wp.append(Wp/(10**9))
        self.list_Wk.append(Wk/(10**9))
        self.list_W.append(W/(10**9))
        self.t += self.dt
        self.list_t.append(self.t)
        self.WT.clear()
        self.WT.set_xlim(0, self.t)
        self.WT.set_title('Энергия системы', fontsize = 20)
        self.WT.set_xlabel('Время, с', fontsize = 15)
        self.WT.set_ylabel('Энергия, ГДж', fontsize = 15)
        self.WT.set_ylim(0, 5000)
        self.WT.plot(self.list_t, self.list_Wp, label = 'Wp(t)')
        self.WT.plot(self.list_t, self.list_Wk, label = 'Wk(t)')
        self.WT.plot(self.list_t, self.list_W, label = 'W(t)')
        self.WT.legend()
        plt.grid()
        plt.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = View()
    sys.exit(app.exec_())
