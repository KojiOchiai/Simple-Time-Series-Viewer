# -*- coding: utf-8 -*-


import sys
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
matplotlib.style.use('ggplot')
import os.path

from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        openAction = QtGui.QAction('&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open CSV File')
        openAction.triggered.connect(self.open_file)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openAction)

        self.graph = Graph(self) 
        self.setCentralWidget(self.graph)
        
        self.setWindowTitle('Simple Time Series Viewer')

    def open_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                     os.path.expanduser('~'))
        # import data
        tsd = pd.DataFrame.from_csv(filename)
        self.graph.plot(tsd)

class Graph(QtGui.QWidget):
    def __init__(self, parent):
        super(Graph, self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # set navigation bar
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self, tsd):
        # data for plot
        time = [mdates.date2num(idx.to_datetime()) for idx in tsd.index]
        y1 = tsd['brightness'].as_matrix()
        y2 = tsd['temperature'].as_matrix()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.hold(True)
        ax.plot_date(time, y1, 'b-')
        ax.plot_date(time, y2, 'g-')
        self.figure.autofmt_xdate()
        
        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())


