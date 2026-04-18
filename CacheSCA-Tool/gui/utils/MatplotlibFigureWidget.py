from PyQt5 import QtWidgets

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MatplotlibFigureWidget(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(MatplotlibFigureWidget, self).__init__(parent)

		self.figure = Figure()
		self.canvas = FigureCanvas(self.figure)

		self.setLayout(QtWidgets.QVBoxLayout())
	
	def enableToolBar(self):
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.layout.addWidget(self.toolbar)
	
	def setLayout(self, layout):
		self.layout = layout
		self.layout.addWidget(self.canvas)
		super(MatplotlibFigureWidget, self).setLayout(self.layout)
	
	def add_subplot(self, *args, **kwargs):
		return self.figure.add_subplot(*args, **kwargs)

	def draw(self):
		self.canvas.draw()
