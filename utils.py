from math import sqrt

class Chastica():
    def __init__(self, m, i, j, k, l, radio_check):
        self.m = m
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.Vx = 0
        self.Vy = 0
        if radio_check[0]:
            self.x = l*j+(i+1)%2*(l/2)
            self.y = sqrt(l**2-(l/2)**2)*i
            self.z = 0
        elif radio_check[1]:
            self.x = l*j
            self.y = l*i
            self.z = 0
        elif radio_check[2]:
            self.x = l*j+(i+1)%2*l/2+(j+1)//2*l
            if i%2 == 0 and j%2 == 1:
                self.x -= l
            self.y = sqrt(l**2-(l/2)**2)*i
            self.z = 0
        self._x_ = self.x
        self._y_ = self.y
        self._z_ = self.z
        self.Fx = 0
        self.Fy = 0
        self.pause = False

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

    def move(self, dt):
        if not self.pause:
            _x_ = self._x_
            _y_ = self._y_
            self._x_ = self.x
            self._y_ = self.y
            self.x = 2*self.x-_x_+(self.Fx/self.m)*(dt**2)
            self.y = 2*self.y-_y_+(self.Fy/self.m)*(dt**2)
            
        
class Reshetka():
    def __init__(self, a, b, dt, l, k, m, radio_check):
        self.a = a
        self.b = b
        self.dt = dt
        self.l = l
        self.k = k
        self.m = m
        self.radio_check = radio_check
        self.matrix = self.create_matrix()

    def create_matrix(self):
        return [[Chastica(self.m, i, j, self.k, self.l, self.radio_check) for j in range(self.b)] for i in range(self.a)]

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
        if self.radio_check[0]:
            for b in range(2):
                particles.append(self.matrix[i][j+(-1)**b])
            for a in range(2):
                for b in range(2):
                    if i%2 == 0:
                        particles.append(self.matrix[i+(-1)**a][j+b])
                    else:
                        particles.append(self.matrix[i+(-1)**a][j-b])
        elif self.radio_check[1]:
            for a in range(2):
                particles.append(self.matrix[i+(-1)**a][j])
            for b in range(2):
                particles.append(self.matrix[i][j+(-1)**b])
        elif self.radio_check[2]:
            if j%2 == 1:
                particles.append(self.matrix[i][j-1])
            else:
                particles.append(self.matrix[i][j+1])
            for a in range(2):
                particles.append(self.matrix[i+(-1)**a][j])
        return particles
