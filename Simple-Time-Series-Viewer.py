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
        self.setCentralWidget(self.graph)
        self.setWindowTitle('Simple Time Series Viewer')

    def open_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                     os.path.expanduser('~'))
        # import data
        self.statusBar().showMessage('loading data...')
        data = pd.DataFrame.from_csv(filename)
        self.statusBar().showMessage('')
        self.statusBar().showMessage('ploting...')
        self.graph.set_data(data)
        self.graph.column_plot = [[data.columns[0]], [data.columns[1]]]
        self.graph.plot()
        self.statusBar().showMessage('')

class Graph(QtGui.QWidget):
    def __init__(self, parent):
        super(Graph, self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self._data = None
        self.column_plot = [[]]

        # set navigation bar
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.pan()

        # column list
        self.column_list = QtGui.QListWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Expanding)
        self.column_list.setSizePolicy(sizePolicy)
        
        # add buttun
        self.add_button = QtGui.QPushButton('add axis')
        self.del_button = QtGui.QPushButton('delete axis')

        # set the layout
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(self.toolbar)
        vlayout.addWidget(self.canvas)
        button_layout = QtGui.QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.del_button)
        vlayout.addLayout(button_layout)        

        hlayout = QtGui.QHBoxLayout()
        hlayout.addLayout(vlayout)
        hlayout.addWidget(self.column_list)
        self.setLayout(hlayout)

    def set_data(self, data):
        self._data = data
        for label in self._data.columns:
            item = QtGui.QListWidgetItem(label)
            self.column_list.addItem(item)

    def get_Data(self):
        return self._data

    def plot(self):
        if self._data.empty:
            return
        
        n_subplot = len(self.column_plot)
        for n_row, columns in enumerate(self.column_plot):
            # create an axis
            if n_row == 0:
                ax = self.figure.add_subplot(n_subplot, 1, n_row+1)
                # save first axis for link axis
                ax1 = ax
            else:
                ax = self.figure.add_subplot(n_subplot, 1, n_row+1,
                                             sharex=ax1)

            # discards the old graph
            ax.hold(False)
            
            for column_name in columns:
                # data for plot
                time = [mdates.date2num(idx.to_datetime())
                        for idx in self._data.index]
                y = self._data[column_name].as_matrix()
                
                # plot data
                ax.hold(True)
                ax.plot_date(time, y, '-', label=column_name)
                self.figure.autofmt_xdate()

            plt.legend()
        
        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())


