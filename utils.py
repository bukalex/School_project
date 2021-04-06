from math import sqrt
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QMouseEvent

class Chastica():
    def __init__(self, m, i, j, k, l, radio_check):
        self.m = m
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.Vx = 0
        self.Vy = 0
        self.V = 0
        if radio_check[0]:
            self.x = l*j+(i+1)%2*(l/2)+300
            self.y = sqrt(l**2-(l/2)**2)*i+50
            self.z = 0
        elif radio_check[1]:
            self.x = l*j+300
            self.y = l*i+50
            self.z = 0
        elif radio_check[2]:
            self.x = l*j+(i+1)%2*l/2+(j+1)//2*l+300
            if i%2 == 0 and j%2 == 1:
                self.x -= l
            self.y = sqrt(l**2-(l/2)**2)*i+50
            self.z = 0
        self.x_ = self.x
        self.y_ = self.y
        self.z_ = self.z
        self.Fx = 0
        self.Fy = 0
        self.pause = False

    def sily(self, particles, dt):
        self.Fx = 0
        self.Fy = 0
        for part in particles:
            d = sqrt((part.x-self.x)**2+(part.y-self.y)**2)
            if d != 0:
                dx = (d-self.l)*(part.x-self.x)/d
                dy = (d-self.l)*(part.y-self.y)/d
                self.Fx += self.k*(d-self.l)*(part.x-self.x)/d
                self.Fy += self.k*(d-self.l)*(part.y-self.y)/d
                self.Vx += dt*self.Fx/self.m
                self.Vy += dt*self.Fy/self.m

    def move(self, dt):
        if not self.pause:
            x_ = self.x_
            y_ = self.y_
            self.x_ = self.x
            self.y_ = self.y
            self.x = 2*self.x-x_+(self.Fx/self.m)*(dt**2)
            self.y = 2*self.y-y_+(self.Fy/self.m)*(dt**2)

            
class Lines():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.L = sqrt((x1-x2)**2+(y1-y2)**2)

    
class Reshetka():
    def __init__(self, a, b, dt, l, k, m, radio_check):
        self.a = a
        self.b = b
        self.dt = dt
        self.l = l
        self.k = k
        self.m = m
        self.radio_check = radio_check
        self.Wp = 0
        self.Wk = 0
        self.W = 0
        self.matrix = self.create_matrix()
        self.lines = self.create_lines()

    def create_matrix(self):
        return [[Ellipse(self.m, i, j, self.k, self.l, self.radio_check, self.a, self.b) for j in range(self.b)] for i in range(self.a)]

    def create_lines(self):
        lines_list = []
        for i in range(self.a):
            for j in range(self.b):
                if self.radio_check[0]:
                    if i != self.a-1:
                        lines_list.append(Lines(self.matrix[i][j].ell.x+25, self.matrix[i][j].ell.y+25, self.matrix[i+1][j].ell.x+25, self.matrix[i+1][j].ell.y+25))
                    if j != self.b-1:
                        lines_list.append(Lines(self.matrix[i][j].ell.x+25, self.matrix[i][j].ell.y+25, self.matrix[i][j+1].ell.x+25, self.matrix[i][j+1].ell.y+25))
                    if i != self.a-1 and j != self.b-1 and i%2 == 0:
                        lines_list.append(Lines(self.matrix[i][j].ell.x+25, self.matrix[i][j].ell.y+25, self.matrix[i+1][j+1].ell.x+25, self.matrix[i+1][j+1].ell.y+25))
                    if i != self.a-1 and j != 0 and i%2 == 1:
                        lines_list.append(Lines(self.matrix[i][j].ell.x+25, self.matrix[i][j].ell.y+25, self.matrix[i+1][j-1].ell.x+25, self.matrix[i+1][j-1].ell.y+25))
                elif self.radio_check[1]:
                    if i != self.a-1:
                        lines_list.append(Lines(self.matrix[i][j].ell.x+25, self.matrix[i][j].ell.y+25, self.matrix[i+1][j].ell.x+25, self.matrix[i+1][j].ell.y+25))
                    if j != self.b-1:
                        lines_list.append(Lines(self.matrix[i][j].ell.x+25, self.matrix[i][j].ell.y+25, self.matrix[i][j+1].ell.x+25, self.matrix[i][j+1].ell.y+25))
                elif self.radio_check[2]:
                    if i != self.a-1:
                        lines_list.append(Lines(self.matrix[i][j].ell.x+25, self.matrix[i][j].ell.y+25, self.matrix[i+1][j].ell.x+25, self.matrix[i+1][j].ell.y+25))
                    if j != self.b-1 and (i+j)%2 == 0:
                        lines_list.append(Lines(self.matrix[i][j].ell.x+25, self.matrix[i][j].ell.y+25, self.matrix[i][j+1].ell.x+25, self.matrix[i][j+1].ell.y+25))
                    if j != self.b-1 and i%2+j%2 == 2:
                        lines_list.append(Lines(self.matrix[i][j].ell.x+25, self.matrix[i][j].ell.y+25, self.matrix[i][j+1].ell.x+25, self.matrix[i][j+1].ell.y+25))
        return lines_list

    def step(self):
        for i in range(1, self.a-1):
            for j in range(1, self.b-1):
                particles = self.get_neighbours(i, j)
                self.matrix[i][j].ell.sily(particles, self.dt)
        for i in range(1, self.a-1):
            for j in range(1, self.b-1):
                self.matrix[i][j].ell.move(self.dt)
        self.lines = self.create_lines()
        self.count_Wp()
        self.count_Wk()
        self.W = self.Wp+self.Wk

    def get_neighbours(self, i, j):
        particles = []
        if self.radio_check[0]:
            for b in range(2):
                particles.append(self.matrix[i][j+(-1)**b].ell)
            for a in range(2):
                for b in range(2):
                    if i%2 == 0:
                        particles.append(self.matrix[i+(-1)**a][j+b].ell)
                    else:
                        particles.append(self.matrix[i+(-1)**a][j-b].ell)
        elif self.radio_check[1]:
            for a in range(2):
                particles.append(self.matrix[i+(-1)**a][j].ell)
            for b in range(2):
                particles.append(self.matrix[i][j+(-1)**b].ell)
        elif self.radio_check[2]:
            if (i + j)%2 == 0:
                particles.append(self.matrix[i][j+1].ell)
            else:
                particles.append(self.matrix[i][j-1].ell)
            for a in range(2):
                particles.append(self.matrix[i+(-1)**a][j].ell)
        return particles

    def count_Wp(self):
        self.Wp = 0
        for i in self.lines:
            self.Wp += 0.5*self.k*(i.L-self.l)**2

    def count_Wk(self):
        self.Wk = 0
        for i in range(self.a):
            for j in range(self.b):
                self.Wk += 0.5*(self.matrix[i][j].ell.Vx**2+self.matrix[i][j].ell.Vy**2)*self.m


class Ellipse(QGraphicsEllipseItem):
    def __init__(self, m, i, j, k, l, radio_check, a, b):
        self.ell = Chastica(m, i, j, k, l, radio_check)
        super().__init__(self.ell.x, self.ell.y, 50, 50)
        if i != 0 and j != 0 and i != a-1 and j != b-1:
            self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.i = i
        self.j = j
        self.a = a
        self.b = b
        self.dx = 0
        self.dy = 0
        self.color = QtGui.QColor(0,0,0)
        self.clicked = False
        self.moved = False

    def mousePressEvent(self, event: QMouseEvent):
        if self.i != 0 and self.j != 0 and self.i != self.a-1 and self.j != self.b-1:
            self.X0 = event.screenPos().x()
            self.Y0 = event.screenPos().y()
            if event.button() == 2:
                if not self.clicked:
                    self.color = QtGui.QColor(150,0,0)
                    self.clicked = True
                else:
                    self.color = QtGui.QColor(0,0,0)
                    self.clicked = False
                self.setBrush(QtGui.QBrush(self.color, style = QtCore.Qt.SolidPattern))

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.i != 0 and self.j != 0 and self.i != self.a-1 and self.j != self.b-1:
            self.dx = event.screenPos().x()-self.X0
            self.dy = event.screenPos().y()-self.Y0
            self.ell.x += self.dx
            self.ell.y += self.dy
            if event.button() == 1:
                self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                if self.moved:
                    self.ell.x -= self.dx
                    self.ell.y -= self.dy
                self.moved = True


class Line(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
