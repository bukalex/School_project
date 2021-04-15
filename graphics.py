from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Energy(QDialog):           # диалоговое окно для вывода графиков
    def __init__(self, list_Wp, list_Wk, list_W, list_Mx, list_My, list_t, t):
        super().__init__()
        self.resize(1400, 500)
        self.setWindowTitle('Графики')
        self.list_Wp = list_Wp
        self.list_Wk = list_Wk
        self.list_W = list_W
        self.list_Mx = list_Mx
        self.list_My = list_My
        self.list_t = list_t
        self.t = t
        self.WT = PlotCanvas(self, width=7, height=5)           # вывод графика зависимости энергии от времени
        self.MT = PlotCanvas(self, width=7, height=5)           # вывод графика зависимости момента энергии от времени
        self.WT.plot_WT()
        self.MT.plot_MT()
        self.MT.move(700, 0)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent, width, height, dpi=100):             # связь matplotlib с PyQt5
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.parent = parent

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def plot_WT(self):           # график зависимости энергии от времени
        self.axes.set_title('Энергия системы', fontsize = 20)
        self.axes.set_xlabel('Время, с', fontsize = 15)
        self.axes.set_ylabel('Энергия, *10^-40 Дж', fontsize = 15)
        self.axes.set_ylim(0, max(self.parent.list_W)+200)
        self.axes.set_xlim(0, self.parent.t)
        self.axes.plot(self.parent.list_t, self.parent.list_Wp, label = 'Wp(t)')
        self.axes.plot(self.parent.list_t, self.parent.list_Wk, label = 'Wk(t)')
        self.axes.plot(self.parent.list_t, self.parent.list_W, label = 'W(t)')
        self.axes.grid()
        self.axes.legend()
        self.draw()

    def plot_MT(self):           # график зависимости момента энергии от времени
        self.axes.set_title('Центр энергии системы', fontsize = 20)
        self.axes.set_xlabel('Время, с', fontsize = 15)
        self.axes.set_ylabel('Центр энергии, *10^-11 м', fontsize = 15)
        self.axes.set_ylim(0, max(self.parent.list_Mx+self.parent.list_My)+200)
        self.axes.set_xlim(0, self.parent.t)
        self.axes.plot(self.parent.list_t, self.parent.list_Mx, label = 'Mx(t)')
        self.axes.plot(self.parent.list_t, self.parent.list_My, label = 'My(t)')
        self.axes.grid()
        self.axes.legend()
        self.draw()
