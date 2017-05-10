#! /usr/bin/env python3

import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QApplication, QPushButton, QWidget, QHBoxLayout, \
    QVBoxLayout

__author__ = "Grzegorz Bokota"


class MainWindow(QMainWindow):
    def __init__(self, name):
        super(MainWindow, self).__init__()
        self.setWindowTitle(name)
        self.cmap = "viridis"  # pyplot.colormaps() - list of all colormaps
        self.matrix_size = 20
        self.matrix = np.diag(np.ones(self.matrix_size)) + np.diag(np.ones(self.matrix_size - 1), -1) \
                      + np.diag(np.ones(self.matrix_size - 1), 1)

        self.matrix = self.matrix.astype(np.bool)

        self.new_matrix_btn = QPushButton("New matrix")
        self.new_matrix_btn.clicked.connect(self.set_size)
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save)
        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self.load)

        fig = pyplot.figure(figsize=(6, 6), dpi=100, frameon=False, facecolor='1.0', edgecolor='w',
                            tight_layout=True)
        self.figure_canvas = FigureCanvas(fig)
        self.fig_num = fig.number
        pyplot.imshow(self.matrix, self.cmap)

        self.figure_canvas.mpl_connect('button_press_event', self.draw)

        central_widget = QWidget()
        main_layout = QVBoxLayout()
        btn_lay = QHBoxLayout()
        btn_lay.addWidget(self.new_matrix_btn)
        btn_lay.addWidget(self.save_btn)
        btn_lay.addWidget(self.load_btn)
        main_layout.addLayout(btn_lay)
        main_layout.addWidget(self.figure_canvas)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def re_draw(self):
        fig = pyplot.figure(self.fig_num)
        pyplot.imshow(self.matrix, cmap=self.cmap) # imshow has argument cmap 
        fig.canvas.draw()

    def save(self):
        dial = QFileDialog(self, "Save file")
        dial.setFileMode(QFileDialog.AnyFile)
        dial.setAcceptMode(QFileDialog.AcceptSave)
        dial.setNameFilter("restraints (*.npy)")
        if dial.exec_():
            file_path = str(dial.selectedFiles()[0])
            np.save(file_path, self.matrix)

    def load(self):
        dial = QFileDialog(self, "load file")
        dial.setFileMode(QFileDialog.ExistingFile)
        dial.setNameFilter("numpy array (*.npy)")
        if dial.exec_():
            file_path = str(dial.selectedFiles()[0])
            self.matrix = np.load(file_path)
            self.matrix_size = self.matrix.shape[0]
            self.re_draw()

    def set_size(self):
        res = QInputDialog.getInt(self, "Set contact map size", "Size", self.matrix_size, 2, 500, 1)
        if res[1]:
            self.matrix_size = res[0]
            self.matrix = np.diag(np.ones(self.matrix_size)) + np.diag(np.ones(self.matrix_size - 1), -1) \
                          + np.diag(np.ones(self.matrix_size - 1), 1)
            self.matrix = self.matrix.astype(np.bool)
            self.re_draw()

    def draw(self, event):
        if event.xdata is not None and event.ydata is not None:
            ix, iy = int(event.xdata + 0.5), int(event.ydata + 0.5)
            if ix == iy or ix + 1 == iy or ix - 1 == iy:
                return
            val = not self.matrix[ix, iy]
            self.matrix[ix, iy] = val
            self.matrix[iy, ix] = val
            self.re_draw()


if __name__ == '__main__':
    import sys

    myApp = QApplication(sys.argv)
    wind = MainWindow("Prepare contact map")
    wind.show()
    myApp.exec_()
    sys.exit()
