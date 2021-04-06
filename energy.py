import math

from PIL import ImageGrab
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QDoubleSpinBox, \
    QLabel, QFileDialog, QAbstractItemView, QTreeView, QListView, QDialog, QCheckBox


class EnergyApp(QDialog):
    rs_signal = QtCore.pyqtSignal(QtCore.QSize)

    def __init__(self):
        super(EnergyApp, self).__init__()
        self.layout = QVBoxLayout()
        # Latitude selection
        self.spinBox1 = QDoubleSpinBox(self)
        # Longitude selection
        self.spinBox2 = QDoubleSpinBox(self)
        # Time horizont selection
        self.spinBox3 = QDoubleSpinBox(self)
        # Scaling spinBox
        self.spinBox4 = QDoubleSpinBox(self)
        self.keepDraw = False
        self.start = QPoint()
        self.end = QPoint()
        # self.resize(950, 720)
        self.setFixedSize(1100, 720)
        self.move(100, 100)
        self.setWindowTitle("Scenario drawer")
        self.setMouseTracking(True)
        self.type = 'our'
        self.image = []
        self.index = []
        # Scale: pixels in nm
        self.scale = 5
        # Preferred number of lines in grid
        self.n_line_x = 10
        self.n_line_y = 10
        # Time horizon
        self.time_horizon = 2
        # Flag if output dir is select
        # Default state is returned in clear_window()
        self.dir_select = False
        # Path to output dir
        self.path = ''
        # Flag if new ship is entered
        self.proc_draw = False
        # Ship params from dialog
        self.vel = 0
        self.heading = 0
        # Velocity of our ship
        # self.v0 = Vector2(0, 0)
        # Some hotfix flag
        self.first = True
        # Changing ship params
        self.onParamChange = False
        # Flag for rotating drawing field:
        self.nord = True
        # Future checkbox:
        self.orientation = None
        # Heading offset
        self.offset = 0
        # Drawing polygon flag
        self.drawing_poly = False
        # Index with polygons
        self.poly_index = []
        # Polygon points
        self.ppoints = []
        self.initUI()

    def initUI(self):
        imageSize = QtCore.QSize(1366, 768)
        self.image = QtGui.QImage(imageSize, QtGui.QImage.Format_RGB32)
        self.image.fill(QtGui.qRgb(255, 255, 255))

        # Resize signal
        self.rs_signal.connect(self.resize_grid)

        # Clear button
        button = QPushButton('Clear field', self)
        button.move(0, 0)
        button.resize(140, 50)
        button.clicked.connect(self.clear_window)

        # Convert button
        button1 = QPushButton('Convert', self)
        button1.move(140, 0)
        button1.resize(140, 50)
        button1.clicked.connect(self.open_or_create_directory)

        # Latitude spinbox
        lbe = QLabel(self)
        lbe.setText('Start Latitude:')
        lbe.move(280, 5)
        self.spinBox1.setRange(0, 360)
        self.spinBox1.move(400, 0)
        self.spinBox1.setValue(60)
        self.spinBox1.setSingleStep(0.01)

        # Longitude spinbox
        lbe1 = QLabel(self)
        lbe1.setText('Start Longitude:')
        lbe1.move(280, 30)
        self.spinBox2.setRange(0, 360)
        self.spinBox2.move(400, 25)
        self.spinBox2.setValue(30)
        self.spinBox2.setSingleStep(0.01)

        self.draw_poly = QPushButton('Draw Polygon', self)
        self.draw_poly.move(0, 50)
        self.draw_poly.clicked.connect(self.draw_polygon)

        self.viz = QPushButton('Create new ship', self)
        self.viz.move(500, 0)
        self.viz.resize(140, 50)
        # self.viz.clicked.connect(self.create_ship)

        # Time horizon values
        lbe3 = QLabel(self)
        lbe3.setText('Time horizon:')
        lbe3.move(650, 5)
        self.spinBox3.setRange(0, 10)
        self.spinBox3.move(765, 0)
        self.spinBox3.setValue(2)
        self.spinBox3.setSingleStep(0.01)

        # Scaling params
        lbe4 = QLabel(self)
        lbe4.setText('Scale, nm in sq:')
        lbe4.move(650, 30)
        self.spinBox4.setRange(0.01, 1000)
        self.spinBox4.move(765, 25)
        self.spinBox4.setValue(self.scale)
        self.spinBox4.setSingleStep(0.1)
        # self.spinBox4.valueChanged.connect(self.update_scale)

        # Rotation grid params
        self.orientation = QCheckBox("South-north", self)
        self.orientation.move(880, 2)
        self.orientation.toggle()
        # self.orientation.stateChanged.connect(self.change_orientation)

        # Angle dispay
        lbe5 = QLabel(self)
        lbe5.move(880, 30)
        lbe5.setText("Angle: ")
        self.m_peleng = QLabel(self)
        self.m_peleng.move(930, 30)
        self.m_peleng.setText("NODATA")

        # Dist display
        lbe6 = QLabel(self)
        lbe6.move(880, 50)
        lbe6.setText("Dist: ")
        self.m_dist = QLabel(self)
        self.m_dist.move(930, 50)
        self.m_dist.setText("NODATA")

        # Course angle display
        lbe7 = QLabel(self)
        lbe7.move(880, 70)
        lbe7.setText("CAng: ")
        self.m_course = QLabel(self)
        self.m_course.move(930, 70)
        self.m_course.setText("NODATA")

        self.draw_grid()

    def open_or_create_directory(self):
        """
        Creates dialog with output directory selection
        :return:
        """
        img = ImageGrab.grab()
        if not self.dir_select:
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.DontUseNativeDialog, True)

            l = dialog.findChild(QListView, "listView")
            if l is not None:
                l.setSelectionMode(QAbstractItemView.MultiSelection)
            t = dialog.findChild(QTreeView)
            if t is not None:
                t.setSelectionMode(QAbstractItemView.MultiSelection)

            nMode = dialog.exec_()
            self.path = dialog.selectedFiles()[0]
            self.dir_select = True

        img.save(self.path + "/scenario.jpeg", "JPEG")
        self.convert_file(self.path)

    def resizeEvent(self, event):
        """
        event onResize
        :param event:
        :return:
        """
        self.rs_signal.emit(self.size())

    def resize_grid(self):
        """
        re-draws grid for new size
        :return:
        """
        self.clear_window(True)
        self.draw_grid()
        self.plot_all_targets()

    def clear_window(self, upd=False, painter=None):
        """
        Cleares window and sets some flags to default
        :param upd: flag to recreate self.index
        :return:
        """
        self.image.fill(QtGui.qRgb(255, 255, 255))
        if not upd:
            self.type = 'our'
            self.index = []
            self.spinBox4.setDisabled(False)
            self.orientation.setDisabled(False)
        else:
            self.plot_all_targets(painter)
            self.plot_all_polygons(painter)
        self.draw_grid(painter)
        self.update()
        self.dir_select = False

    def plot_all_polygons(self, painter=None):
        """
        Plots all polygons
        :param painter:
        :return:
        """
        if painter is None:
            painter = QPainter(self.image)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.BDiagPattern))
        for obj in self.poly_index:
            painter.drawPolygon(QPolygon(obj['points']))
        painter.setBrush(QBrush(Qt.red, Qt.NoBrush))

    def draw_polygon(self):
        """
        Activates drawing polygon mode
        :return:
        """
        self.drawing_poly = True
        self.draw_poly.setDisabled(True)

    def draw_grid(self, painter=None):
        """
        This function draws nm grid
        :return:
        """
        if painter is None:
            painter = QPainter(self.image)
        # Optimal step — 60 pixels
        optimal_step = 60
        self.n_line_x = round(self.width() / optimal_step)
        self.n_line_y = round(self.height() / optimal_step)
        stepw = steph = optimal_step
        self.scale = steph / self.spinBox4.value()
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        pen.setStyle(Qt.DashDotDotLine)
        painter.setPen(pen)
        for i in range(self.n_line_x + 1):
            painter.drawLine(i * stepw, 0, i * stepw, self.height())
            painter.drawText(i * stepw, self.n_line_y * steph - 10,
                             str(round(i * stepw / self.scale, 2)))
        for i in range(self.n_line_y + 1):
            painter.drawLine(0, i * steph, self.width(), i * steph)
            painter.drawText(self.n_line_x * stepw - 40, self.height() - i * steph,
                             str(round(i * steph / self.scale, 2)))

    def closeEvent(self, event):
        print("Closed")

    def plot_all_targets(self, painter=None):
        """
        This function plots all obj in self.index after resize
        :return:
        """
        if painter is None:
            painter = QPainter(self.image)
        for obj in self.index:
            if obj['type'] == 'our':
                pen = QPen(Qt.red, 2, Qt.SolidLine)
                painter.setPen(pen)
            else:
                pen = QPen(Qt.blue, 2, Qt.SolidLine)
                painter.setPen(pen)
            start = QPoint()
            end = QPoint(obj['end'][0], obj['end'][1])
            start.setX(end.x() + 30 * math.cos(math.radians(obj['heading'] - 90
                                                            + self.offset)))
            start.setY(end.y() + 30 * math.sin(math.radians(obj['heading'] - 90
                                                            + self.offset)))
            painter.drawLine(start, end)
            painter.drawEllipse(end, 10, 10)

    def paintEvent(self, event):
        """
        Event handler for painter
        :param event:
        :return:
        """
        painter = QPainter(self)
        cur_size = QRect(0, 0, self.width(), self.height())
        temp = self.image.copy(cur_size)
        painter.drawImage(event.rect(), temp)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.proc_draw:
            self.keepDraw = True
            self.end = event.pos()
            print(self.orientation.isChecked())
            if not self.orientation.isChecked():
                if self.type == 'our':
                    self.offset = -self.heading
                    self.heading = 0
            self.start.setX(self.end.x() + 30 * math.cos(math.radians(self.heading - 90)))
            self.start.setY(self.end.y() + 30 * math.sin(math.radians(self.heading - 90)))
        elif event.button() == QtCore.Qt.RightButton and not self.proc_draw:
            self.onParamChange = True
        elif event.button() == QtCore.Qt.LeftButton and self.drawing_poly:
            self.keepDraw = True
            self.start = event.pos()

    def mouseReleaseEvent(self, event):
        painter = QPainter(self.image)
        if event.button() == QtCore.Qt.LeftButton and self.keepDraw and not self.drawing_poly:
            if self.type == 'our':
                pen = QPen(Qt.red, 2, Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(self.start, self.end)
                painter.drawEllipse(self.end, 10, 10)
                self.index.append({'type': self.type,
                                   'vel': self.vel,
                                   'heading': self.heading - self.offset,
                                   'start': [self.start.x(), self.start.y()],
                                   'end': [self.end.x(), self.end.y()]})
                self.v0 = Vector2(self.vel * math.cos(math.radians(self.heading)),
                                  self.vel * math.sin(math.radians(self.heading)))
                self.type = 'foreign'
            elif self.type == 'foreign':
                pen = QPen(Qt.blue, 2, Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(self.start, self.end)
                painter.drawEllipse(self.end, 10, 10)
                self.index.append({'type': self.type,
                                   'vel': self.vel,
                                   'heading': self.heading - self.offset,
                                   'start': [self.start.x(), self.start.y()],
                                   'end': [self.end.x(), self.end.y()]})
        elif event.button() == QtCore.Qt.LeftButton and self.keepDraw and self.drawing_poly:
            self.draw_poly.setDisabled(False)
            self.drawing_poly = False
            self.poly_index.append({"type": "Polygon",
                                    "points": self.ppoints,
                                    "desc": 'movement_parameters_limitation'})
        if self.onParamChange:
            coords = event.pos()
            for i in range(len(self.index)):
                obj = self.index[i]
                x, y = obj['end'][0], obj['end'][1]
                if coords.x() in range(x - 10, x + 10) and coords.y() in range(y - 10, y + 10):
                    updateDialog = CreateShipDialog()
                    vel, heading = updateDialog.exec_()
                    heading += self.offset
                    self.index[i]['vel'] = vel
                    self.index[i]['heading'] = heading
                    if obj['type'] == 'our':
                        self.v0 = Vector2(vel * math.cos(math.radians(heading)),
                                          vel * math.sin(math.radians(heading)))
                        if not self.orientation.isChecked():
                            self.offset = -(heading - self.offset)
                            self.index[i]['heading'] = -self.offset
                        self.clear_window(upd=True, painter=painter)
                    else:
                        end = QPoint(self.index[i]['end'][0], self.index[i]['end'][1])
                        self.clear_window(upd=True, painter=painter)
                        self.plot_target_info(painter, end, end,
                                              vel, heading)
            self.onParamChange = False
        self.update()
        self.keepDraw = False
        self.proc_draw = False

    def mouseMoveEvent(self, event):
        painter = QPainter(self.image)
        if (event.buttons() & QtCore.Qt.LeftButton) and self.keepDraw and self.proc_draw and not self.drawing_poly:
            self.clear_window(upd=True, painter=painter)
            self.end = event.pos()
            self.start.setX(self.end.x() + 30 * math.cos(math.radians(self.heading - 90)))
            self.start.setY(self.end.y() + 30 * math.sin(math.radians(self.heading - 90)))
            if self.type == 'our' or self.first and not self.onParamChange:
                pen = QPen(Qt.red, 2, Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(self.start, self.end)
                painter.drawEllipse(self.end, 10, 10)
                self.first = False
            elif self.type == 'foreign' and not self.onParamChange:
                self.plot_target_info(painter, self.start, self.end,
                                      self.vel, self.heading)
        elif (event.buttons() & QtCore.Qt.LeftButton) and self.keepDraw and self.drawing_poly:
            self.clear_window(upd=True, painter=painter)
            self.end = event.pos()
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.red, Qt.BDiagPattern))
            # Объявление только так, иначе будет баг с изменением геометрии полигона!!!
            self.ppoints = [
                QPoint(self.start.x(), self.start.y()),
                QPoint(self.start.x(), self.end.y()),
                QPoint(self.end.x(), self.end.y()),
                QPoint(self.end.x(), self.start.y()),
            ]
            painter.drawPolygon(QPolygon(self.ppoints))
        if self.type != 'our':
            our_pose = QPoint(self.index[0]['end'][0], self.index[0]['end'][1])
            end = event.pos()
            dx = end.x() - our_pose.x()
            dy = end.y() - our_pose.y()
            dist = (dx ** 2 + dy ** 2) ** 0.5
            angle = math.degrees(math.atan2(dy, dx)) + 90
            if angle < 0:
                angle += 360
            angle = round(angle, 2)
            cangle = angle - self.index[0]['heading']
            dist = round(dist / self.scale, 2)
            self.m_peleng.setText(str(angle))
            self.m_dist.setText(str(dist))
            self.m_course.setText(str(cangle))
        self.update()
