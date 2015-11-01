# -*- coding: utf-8 -*-


import sys
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
matplotlib.style.use('ggplot')
import os.path

from PyQt4 import QtCore, QtGui
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

        self.statusBar()
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openAction)

        self.graph = Graph(self)
        self.column_list = QtGui.QListWidget()
        self.column_dock = QtGui.QDockWidget("Column List", self)
        self.column_dock.setWidget(QtGui.QListWidget())
        self.setCentralWidget(self.graph)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.column_dock)
        self.setWindowTitle('Simple Time Series Viewer')

    def open_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                     os.path.expanduser('~'))
        # import data
        self.statusBar().showMessage('loading data')
        self.tsd = pd.DataFrame.from_csv(filename)
        self.statusBar().showMessage('')
        self.graph.plot(self.tsd)

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
        y = tsd.iloc[:,0].as_matrix()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.hold(True)
        ax.plot_date(time, y, '-')
        self.figure.autofmt_xdate()
        
        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())


